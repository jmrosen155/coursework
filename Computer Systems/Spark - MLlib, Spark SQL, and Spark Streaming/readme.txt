# The commands to run each part are below. The output will be saved in the ‘output’ folder within the local directory.


# Part 1

spark-submit --master yarn-client p1_tf_idf.py /datasets/hw4/data.txt output/p1_output.txt

# Part 2

spark-submit --master yarn-client p2_kmeans.py /datasets/hw4/data.txt output/p2_output.txt output/p2_output_p3.txt 30

# Part 3

#To put the second output from part 2 onto hdfs for retrieval in the program:
hdfs dfs -put p2_output_p3.txt

spark-submit --master local[2] p3_sql.py p2_output_p3.txt 13478

# Extra credit streaming

spark-submit --master local[2] streaming.py 13478 30