import getopt, sys
import hybrid
import uploadS3
import os
import boto3
import decrypt

def main():
    bucket = None
    object = None
    src = None
    type = None

    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "b:o:f:t:h:")

    except:
        print ("usage: python3 main.py -t upload -b <bucket-name> -o <object>")
        print ("usage: python3 main.py -t download -b <bucket-name> -o <object> -f <file-name>")
        print ("usage: python3 main.py -t decrypt")
        sys.exit(2)

    else:
        for opt, arg in opts:
            if opt in ['-h']:
                print ("usage: python3 main.py -t upload -b <bucket-name> -o <object>")
                print ("usage: python3 main.py -t download -b <bucket-name> -o <object> -f <file-name>")
                print ("usage: python3 main.py -t decrypt")
                os._exit(0)

            elif opt in ['-t']:
                type = arg
            elif opt in ['-b']:
                bucket = arg
            elif opt in ['-o']:
                object = arg
            elif opt in ['-f']:
                src = arg
        if (type == "upload"):
            file_name = hybrid.Encoding()
            uploadS3.upload_file(file_name, bucket, object)
            print("Uploaded Successfully!!!")

        elif (type == "download"):
            s3 = boto3.client('s3')
            s3.download_file(bucket, object, src)
            print("File Downloaded!!!")

        elif (type == "decrypt"):
            decrypt.dec_main()

if __name__ == '__main__':
    main()