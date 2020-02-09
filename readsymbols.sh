while read line
do
 python3 moneycontroldata.py config.ini $line
done < symbols.txt
