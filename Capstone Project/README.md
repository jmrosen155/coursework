# Social Network Analysis of Twitter

The goal of this project was to characterize and map, using network science and text mining techniques, the online Twitter conversation surrounding ‘Data Science’ and ‘Big Data.’ Specifically, we were interested in identifying Twitter influencers in a manner that would facilitate effective marketing campaigns by targeting individuals who can diffuse information in an efficient manner. To this end, the network was constructed by combining the “retweet” and “mention” layers into one projected layer that captures both information diffusion processes. Community structures were identified in the projected network using K-Clique, Modularity, Random Walk, and the Mixed Membership Stochastic Blockmodel. We subsequently identified influencers within each community by utilizing various centrality metrics and analyzed user profiles to gain further insight into the demographics of the communities. Latent Dirichlet Allocation (LDA) was explored in our analysis to incorporate textual data into characterizing the communities. While each of the community detection algorithms we explored has its merits, for our sparse network of tweets, we found that modularity and random walk produced the most coherent communities based on user demographics and influencers. Finally, the network and user demographics of each community were represented in an interactive visualization to allow for further exploration.

*Casey Huang, Yang Liu, Jordan Rosenblum, and Steven Royce*

*[Write-Up](https://cdn.rawgit.com/jmrosen155/coursework/master/Capstone%20Project/TwitterGraph_FinalReport.pdf)*

*[Slides](https://cdn.rawgit.com/jmrosen155/coursework/master/Capstone%20Project/Twitter%20-%20Presentation%2020151214.pdf)*
