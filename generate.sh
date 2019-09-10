#!/bin/bash

TARGET_LANG=$1
BASE_LANG="en_US"

function usage(){
    echo "Usage: bash $0 LANG [FROM_BRANCH]"
    echo "Genetate i18n properties files for LANG language, based on keys found en_US/*.properties  and value from LANG from a previous dataverse-v4.XX branch or specific branch (liek develop)"
    echo "Ex:"
    echo "  bash $0 fr_CA => generate fr_CA from most recent version"
    echo "  bash $0 fr_FR develop => generate fr_FR from develop branch"
    exit 1
}

if [ -z $TARGET_LANG ]; then
    usage
fi

if [ ! -d $BASE_LANG ]; then
    echo "Base language directory is missing: [$BASE_LANG]"
    usage
fi

if [ -d $TARGET_LANG ]; then
    echo "Target language directory already exists. Please delete it manually : rm -r $TARGET_LANG"
    usage
fi

FROM_BRANCH=$2

if [ -z $FROM_BRANCH ];then
    # Detect branch with existing language file
    for version in $(git branch | grep dataverse | sed "s/.*dataverse-\(.*\)/\\1/g"); do
        if [[ "$(git show dataverse-$version: | grep -o $TARGET_LANG)" == "$TARGET_LANG" ]]; then
            FROM_BRANCH=dataverse-$version
        fi
    done
else
    # Check existing language file
    if [[ "$(git show $FROM_BRANCH: | grep -o $TARGET_LANG)" != "$TARGET_LANG" ]]; then
        FROM_BRANCH=""
    fi
fi

if [ -z $FROM_BRANCH ]; then
    echo "Can not find suitable version branch for language $TARGET_LANG"
    exit 1
fi


echo "=== Generate $TARGET_LANG based on branch $FROM_BRANCH"

# Copie reference language files (en_US)
cp -r $BASE_LANG $TARGET_LANG

# Force sed to continue parsing when it hits an “invalid” character
export LANG=C 
find $TARGET_LANG -name '*.properties' -exec sed -i "s/^\([^=]*=\).*$/\\1/g" {} \;

for file in $TARGET_LANG/* ; do
    mv $file ${file/.properties/_$(echo $TARGET_LANG | awk -F '_' '{print $1}').properties}
done


# extract files from original branch
TMP_DIR=$(mktemp -d )
for f in $(git show $FROM_BRANCH:$TARGET_LANG | grep properties); do
    git show $FROM_BRANCH:$TARGET_LANG/$f > $TMP_DIR/$f
done


# fill files
find $TARGET_LANG -name '*.properties' | while read f
do
    CURRENT_FILE=$(basename $f)
    while read originalline
    do
        if [[ "$originalline" =~ ^[a-zA-Z].*$ ]]; then
            targetline=""
            # First search in same fille
            if [ -f $TMP_DIR/$CURRENT_FILE ]; then
                targetline=$(grep -rh "^$originalline" $TMP_DIR/$CURRENT_FILE | head -n 1)
            fi
            if [[ ! -z $targetline ]]; then
                sed -i "s|^$originalline|$targetline|g" $f
            else
                # Second find in all file
                targetline=$(grep -rh "^$originalline" $TMP_DIR/)
                targetline_count=$(grep -rh "^$originalline" $TMP_DIR/ | wc -l)
                if [[ ! -z $targetline && "$targetline_count" -eq "1" ]]; then
                    sed -i "s|^$originalline|$targetline|g" $f
                else
                    echo "Can not translate $f>$originalline"
                fi
            fi
        fi
    done < $f
done

rm -rf $TMP_DIR