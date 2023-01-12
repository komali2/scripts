#! /bin/bash



while read line
	do sed -i -e "1d" $line
done

