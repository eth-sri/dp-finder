#!/bin/bash

# WARNING: May change the permissions and timestamps of files

# sudo apt-get install ruby-dev
# sudo gem install copyright-header

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$BASEDIR"

# cleanup
git clean -xdn

read -p "Cleanup current directory, according to list above? [y/N]" -n 1 -r
echo    # move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]; then
	echo "Cleaning..."
	git clean -xdf
else
	echo "Not cleaning..."
fi

addlicense () {
	FILE="$1"
	COMMENT="$2"
	DRY=n
	NEWFILE="$FILE.newwithlicense"
	if ! grep -q "==BEGIN LICENSE==" "$FILE"; then
		if [[ $DRY =~ ^[Yy]$ ]]; then
			echo "Dry-run: Processing $FILE"
		else
			echo "Processing $FILE"
			# create new file with same permissions
			cp "$FILE" "$NEWFILE"
			# delete file contents
			> "$NEWFILE"
			if [[ "$FILE" = *".sh" ]]; then
				echo "#!/bin/bash" >> "$NEWFILE"
			fi
			cat LICENSE | sed -e "s/^/$COMMENT/" >> "$NEWFILE"
			echo -e "\n" >> "$NEWFILE"
			cat "$FILE" >> "$NEWFILE"
			mv "$NEWFILE" "$FILE"
		fi
	fi
}
export -f addlicense

find . -type f \( \
	-iname \*.py -o \
	-iname Makefile -o \
	-iname Dockerfile -o \
	-iname \*.sh \
	\) -exec bash -c 'addlicense "$0" "# "' {} \;

find . -type f \( \
	-iname \*.psi -o \
	-iname \*.cpp -o \
	-iname \*.h -o \
	-iname \*.hpp \
	\) -not -iname toms462.cpp -not -iname toms462.hpp -exec bash -c 'addlicense "$0" "\/\/ "' {} \;

