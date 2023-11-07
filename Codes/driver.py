import getopt, sys
import file_encrypt
import cloud_upload
import os
import boto3
import full_decrypt

def main():
    bucket = None
    object = None
    src = None
    type = None

    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "b:o:f:t:h:")
        if len(opts)<1:
            print ("Usage: python3 driver.py -h")

    except:
        print ("Usage: python3 driver.py -t upload -b <bucket-name> [-o <object-name on cloud>]")
        print ("Usage: python3 driver.py -t download -b <bucket-name> -o <object-name on cloud> -f <file-name for host>")
        print ("Usage: python3 driver.py -t decrypt")
        sys.exit(2)

    else:
        for opt, arg in opts:
            if opt in ['-h']:
                print ("Usage: python3 driver.py -t upload -b <bucket-name> [-o <object-name on cloud>]")
                print ("Usage: python3 driver.py -t download -b <bucket-name> -o <object-name on cloud> -f <file-name for host>")
                print ("Usage: python3 driver.py -t decrypt")
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
            file_name = file_encrypt.Encoding()
            cloud_upload.upload_file(file_name, bucket, object)
            print("Uploaded Successfully!!!")

        elif (type == "download"):
            s3 = boto3.client('s3')
            s3.download_file(bucket, object, src)
            print("File Downloaded!!!")

        elif (type == "decrypt"):
            full_decrypt.dec_main()
            print("Decryption Successful!!!")

if __name__ == '__main__':
    main()
