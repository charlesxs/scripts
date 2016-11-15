#!/bin/bash
#input a digital convert it to chinese.
#

DigArray=("一" "二" "三" "四" "五" "六" "七" "八" "九")
BaseArray=("个" "十" "百" "千")
GroupArray=(
	[2]="万"
	[3]="亿" 
	[4]="万亿")

GetGroup() {
	local diglen=$1
	beginLen=`awk -v dl=${diglen} 'BEGIN{print dl%4 }'`
	if (( $beginLen >0));then
		key=$((diglen/4 + 1))
	else
		key=$((diglen/4))
	fi
	echo $key
}

#1 0000 0024
#100 0000 00123
Convert() {
	dig=$1
	if grep -q "[^0-9]" <<< $dig;then
		echo "Input error."
		return 1
	fi

	digArray=(`echo $dig | sed 's/[0-9]/& /g'`)
	diglen=${#digArray[*]}
	beginLen=`awk -v dl=${diglen} 'BEGIN{print dl%4}'`

	groupNumer=`GetGroup $diglen`
	current=0
	group=$groupNumer
	for ((i=1;i<=$groupNumer;i++));do
		if (( $beginLen > 0));then
			tArray=(${digArray[*]:$current:$beginLen})
			current=$(($current+$beginLen))
			beginLen=0
		else
			tArray=(${digArray[*]:$current:4})
			current=$(($current+4))
		fi

		tlen=${#tArray[*]}
		index=0
		count=0
		tmpBase=(`echo ${BaseArray[*]:0:$tlen} |rev`)
		for d in ${tArray[*]}; do
			if (($index != $(($tlen-1))));then
				if (($d != 0));then
					if ((count>=1));then
						result=$result"零"${DigArray[$d-1]}${tmpBase[$index]}
						count=0
					else
						result=$result${DigArray[$d-1]}${tmpBase[$index]}
					fi
				else
					((count++))
				fi
			else
				if (($d != 0));then
					if ((count>=1));then
						result=$result"零"${DigArray[$d-1]}${GroupArray[$group]}
						count=0
					else
						result=$result${DigArray[$d-1]}${GroupArray[$group]}
					fi
				else
					((count++))
					if ((count<=3));then
						result=$result${GroupArray[$group]}
					fi
				fi
				((group--))
			fi
			((index++))
		done	
	done
	echo $result
}

Convert $1
echo 
