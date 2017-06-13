Title: Serverless Reddit Crawling With Python And AWS Lambdas
Date: 2017-05-13 10:20
Category: Articles
Status: draft

Amazon recently announced that AWS Lambda now supports Python 3.6, so this is a good
time to explore what we can build with this. I decided to create a data pipeline that 
can be used for crawling top posts from a given Reddit subreddit, and store any linked
images into S3 as a demonstration.

Lambdas are serverless, event-driven elements of the AWS platform, which means you do
not have to worry about where to host the code, and how to scale it out. A simple way to look
at Lambdas is to think of them as cloud-hosted functions that will be called by AWS
infrastructure to respond to some event, e.g. an HTTP call or a timed event.

This article will demonstrate how to use Lambdas to:

* Handle an HTTP request
* Process an SNS event
* Run on a schedule
* Chain Lambdas to process SQS messages

The pipeline will have to accept an HTTP request, triggering the crawl of the specified subreddit. 
This will load the top 100 posts from said subreddit (e.g. XXXXXXX), and then persist all pictures
linked by each of the posts in S3.

The finished pipeline works as follows:
![Reddit Crawler Serverless Pipeline]({filename}/images/reddit-scrape-aws-pipeline-small.png)


1. User POSTs a request to an HTTP endpoint requesting a certain subreddit to be crawled, e.g. /r/aww
2. This request is handled by the first Lambda, titled 'HTTP API Endpoint' in the blueprit. The Lambda will create a new SNS notification, and return a '201 Created' to the user.
3. The SNS event triggers the 'Subreddit Article Loader' Lambda, which will look up the top 100 posts in the given subreddit. It will then enqueue an SQS message for each post. 
4. A Scheduled Lambda ('Article Download Balancer') will periodically check for new work in the SQS queue. When new messages arrive, it will invoke Download Worker Lambdas, handing out one piece of work (i.e a reddit post to process) to ech worker. 
5. Each Worker Lambda will download the pictures linked by the reddit post they were invoked to process, and persist
the files to S3. 
