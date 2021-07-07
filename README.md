# webserver-hash-generator

How to run the program
1.	Simply type “python3 main.py <int: time>”. 
Provide one argument “time” which specifies the expiration time (in second) that you wish the results to be deleted
    a.	Example: “python3 main.py 60” means the created results will be deleted after 60 seconds

2.	Go to http://127.0.0.1:5000/ to upload you file

3.	Once you upload the file successfully, you will get a token.

4.	Get the hash by browsing http://127.0.0.1:5000/<int:token>/<string:hash_type>

    a.	where “token” is the token that you just obtained and “hash_type” can be one of these three: md5, sha1 or sha256. You must provide these two parameters.
    <br>
    b.	An example would be: http://127.0.0.1:5000/1/md5
