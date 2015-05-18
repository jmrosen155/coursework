The commands to run parts 3 and 4 are below:

# Part 3

hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar -input /datasets/test/pg1342.txt -output output/3_gram -mapper wc_mapper.py -reducer wc_reducer.py -file wc_mapper.py -file wc_reducer.py

#The below line is optional just to get the intermediate file to your local system
hdfs dfs -get output/3_gram

hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar -D mapreduce.job.reduces=1 -input output/3_gram/part-00000 -output output/top_10 -mapper wc_mapper1.py -reducer wc_reducer1.py -file wc_mapper1.py -file wc_reducer1.py

hdfs dfs -get output/top_10

nano top_10/part-00000

# Part 4
# I ran the analysis on the sample_data and my output is attached.

hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar -D mapreduce.job.reduces=8 -input /datasets/en_wikipedia_dump/sample_data/ -output output/5_gram -mapper wiki_mapper.py -reducer wiki_reducer.py -file wiki_mapper.py -file wiki_reducer.py

#The below line is optional just to get the intermediate file to your local system
hdfs dfs -get output/5_gram

hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar -D mapreduce.job.reduces=1 -input output/5_gram/part-00000 -output output/top_5 -mapper wiki_mapper1.py -reducer wiki_reducer1.py -file wiki_mapper1.py -file wiki_reducer1.py

hdfs dfs -get output/top_5

nano top_5/part-00000