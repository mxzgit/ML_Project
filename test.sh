for i in $(seq 5524 5620)
do
        ./darknet detector test cfg/cheackboard.data cfg/board2.cfg backup/board2_990.weight test_new/8D5U$i
        cp predictions.jpg results/$i.jpg
done 

for i in $(seq 281 903)
do
        ./darknet detector test cfg/cheackboard.data cfg/board2.cfg backup/board2_990.weight test_new/IMG_0$i
        cp predictions.jpg results/$i.jpg
done
