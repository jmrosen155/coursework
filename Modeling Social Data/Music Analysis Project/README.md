#Music Recommendation System using the Million Song Dataset (last.fm)

*Erin Grand, Justin Law, and Jordan Rosenblum*

Used collaborative filtering algorithms that utilize user feedback in order to predict what songs users may like. For benchmarking the algorithms, we used a Mean Average Precision score truncated at 500 recommended songs. It was discovered that probabilistic matrix factorization with a MAP value of 0.014 did not improve results much from using a baseline of simply recommending popular songs, while artist-based popularity along with user-based and item-based collaborative filtering methods yielded much better results, with the best method giving a MAP value of 0.048.

*[Write-Up](https://cdn.rawgit.com/jmrosen155/coursework/master/Modeling%20Social%20Data/Music%20Analysis%20Project/MSDgroupwriteup.pdf)*
