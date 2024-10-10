dir="/path/to/exonerate_out/*.fas"

for x in $dir
do
    grep "^>" $x | awk '{ print($5) }'| sort -n | tail -1 > max.out
    grep -w -P -f max.out $x > list_of_headers.txt
    awk '/^>/ {printf("\n%s\n",$0);next; } { printf("%s",$0);}  END {printf("\n");}' $x | tail -n +2 > "${x%.*}_SL.fas"
    grep -A1 -f list_of_headers.txt "${x%.*}_SL.fas" > "${x%.*}_max.fas"
    rm $x
done
