#! /bin/bash



while read line
	do sed -i '1s;^;import SegmentIconButton from "ui-component/SegmentIconButton"\n;' $line
done

