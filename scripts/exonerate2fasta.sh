dir="/path/to/exonerate_out/*.out"

for x in $dir
do
	sed -n '/^>/,/^$/p' $x > "${x%.*}".fas
done
