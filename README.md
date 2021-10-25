## EaglesOnboardingTasks

1. sync_mail : Play Around with Gmail API's. For Example, take a group of 2-3 emails, and whenever any new email with a particular subject comes to the any of the users, that email should be synced to the other grouped users.
    - install requirements.txt
        ``` 
        pip3 install -r requirements.txt
        ```
    - Keep the secret token files for all the user's in the same directory
    - Run the Script and create the pickle file's for all the user's.
    - Finally, Re-Run the Script to Sync Mail
        ``` 
        python3 sync_mail.py
        ```

2. RabbitMQ : Basics of RabbitMQ.
    - Basic Hello World Program to Send and Receive messages using RabbitMQ.
    - Work queues: Distributing tasks among workers 
    - Publish/Subscribe: Sending messages to many consumers at once
    - Routing: Receiving messages selectively
    - Topics: Receiving messages based on a pattern (topics)
    - RPC: Request/reply pattern example
    #### install requirements.txt
    ``` 
    pip3 install -r requirements.txt
    ```

3. Kafka : Application to Stream Video's with confluent (using consumer, producer and a topic)
    - Download and Install confluent Platform in the Kafka folder itself.
    - Start confluent services/platform
        ``` 
        confluent local services start
        ```
    - Set up a topic in consumer and send a video file
        ``` 
        python3 consumer.py
        ```
    - To publish a video file to kafka server
        ``` 
        python3 producer.py
        ```
