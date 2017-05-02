Title: Serverless Reddit Crawling With Python And AWS Lambdas
Date: 2017-05-13 10:20
Category: Articles

Amazon recently announced that AWS Lambda now supports Python 3.6, so this is a good
time to explore what we can build with this. I decided to create a data pipeline that 
can be used for scraping top posts from a given Reddit subreddit, and store any linked
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

The finished pipeline looks as follows:
-PICTURE HERE-


