#!/bin/bash

# Parameters
repo=mozilla-mobile/mozilla-vpn-client
workflow=Sources
releases=releases.json
build=${DESTDIR:-build}

# Curl common args to access the GH API as an array
curl=(curl -s -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28")
# You may skip tokens, or use one from env, etc.
if [ -n "$GITHUB_TOKEN" ]; then
	curl+=(-H "Authorization: Bearer $GITHUB_TOKEN")
else
	curl+=(-H "Authorization: Bearer `kwallet-query -r cimbali@github kdewallet`")
fi

# Bail if anything goes wrong
set -e

mkdir -p "$build/"

# Fetch/get tag
if (( $# )); then
	tag=$1
	shift

	if [[ "$tag" =~ ^v[0-9]+(\.[0-9]+){2}$ ]]; then
		echo Using tag $tag
	else
		echo "Tag $tag does not fit the expected format 'v{Major}.{Minor}.{Patch}'"
		exit 1
	fi
else
	"${curl[@]}" "https://api.github.com/repos/$repo/releases" -o "$build/$releases"
	tag=`jq -r '.[0].tag_name' "$build/$releases"`
	echo Latest tag fetched: $tag
fi


# Ensure we have the right files
orig=mozillavpn_${tag#v}.orig.tar.gz
pack=Sources_${tag#v}.zip
spec=mozillavpn.spec
changes=mozillavpn.changes

if [ ! -f "$build/$pack" ]; then
	for (( page=1 ; page < 10 ; ++page )); do
		rel=`"${curl[@]}" "https://api.github.com/repos/$repo/actions/artifacts?name=$workflow&per_page=100&page=$page" |
			jq -r ".artifacts[] | select(.workflow_run.head_branch == \"releases/${tag#v}\")"`
		[ -n "$rel" ] && break
	done

	if [ -z "$rel" ]; then
		echo "Could not find action artifact!"
		exit 1
	fi

	url=`echo "$rel" | jq -sr '.[0].archive_download_url'`
	# Get Location: header, watch out for CRLF end lines
	dl=`"${curl[@]}" -D - "$url" | awk -F '[ \n\r\t]' 'tolower($1) == "location:" { print $2 }'`

	# non-silent curl
	curl "$dl" -o "$build/$pack"
else
	echo Source bundle already downloaded
fi

if [ ! -f "$build/$orig" ]; then
	base="${orig%.orig.tar.gz}"
	actual_orig=$(unzip -l "$build/$pack" | grep -oE "${base}(~rc[0-9]+)?\.orig\.tar\.gz")
	unzip -o "$build/$pack" "$actual_orig"
	if [ "$actual_orig" != "$orig" ]; then
		actual_base="${actual_orig%.orig.tar.gz}"
		tar xf "$actual_orig" --transform "s@^${actual_base/_/-}@${base/_/-}@"
		tar czf "$build/$orig" "${base/_/-}/"
		rm -r "$actual_orig" "${base/_/-}/"
	else
		mv "$actual_orig" "$build/$orig"
	fi
else
	echo Source code already extracted
fi

# If running CI, just exit after downloading files
if [ -n "$CI" ]; then
	ls -l "$build/$orig"
	exit 0
fi

# Extract spec file
unzip -o "$build/$pack" "$spec"
ls -l "$build/$orig" "$spec"

# Manual steps
# import spec file updates
vim "$spec" +Gdiff

(
# Prepend version item to changelog
echo "- Update to version $tag"
# Also prepend pandoc-wrapped (for list awareness) body of github release
jq -r '.[0].body' "$build/$releases" | sed -r \
	-e 's/^[-*]/  &/;s/\r$//;/What.s New|Full Changelog|Downloads at/d;/New Contributors/,/^$/d' \
	-e 's,(#|https://github.com/mozilla-mobile/mozilla-vpn-client/pull/)([0-9]+),gh#\2,'
) | pandoc --from=markdown --to=markdown --columns=70 |
	sed -r 's/^ {8}/    /;s/^- {3}/- /;s/^ {4}- {3}/  * /;$a\\' |
	sed -i '0r/dev/stdin' "$changes"

# Update changelog
osc vc

# Build source rpm
spec-cleaner "$spec" > "$build/$spec"

absbuild="`readlink -f "$build"`"
git ls-files -z \*.patch | xargs -r0 cp -t "$absbuild/"
rpmbuild -D "_topdir $absbuild" -D "_sourcedir $absbuild" -D "_srcrpmdir $absbuild" -bs "$build/$spec"

git commit -em "Version $tag" "$spec" "$changes"
