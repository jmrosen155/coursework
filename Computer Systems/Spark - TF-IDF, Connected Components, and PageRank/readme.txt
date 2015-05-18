# The commands to run each part are below. The output will be saved in the ‘output’ folder within the local directory.


# Part 1

spark-submit --master yarn-client p1_tf_idf.py /datasets/hw3/p1_dataset/p1_data.xml

# Part 2

spark-submit --master yarn-client p2_cc.py /datasets/hw3/p2_dataset/p2_data.xml 0.3

# Part 3

spark-submit --master yarn-client p3_pagerank.py /datasets/hw3/p3_dataset/page_files/p3_data.xml 0.2 /datasets/hw3/p3_dataset/page_link.txt 10