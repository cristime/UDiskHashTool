import sys
import os
import hashlib
from argparse import ArgumentParser
from pathlib import Path


class FileHash:
    def __init__( self, rootdir: str ) -> None:
        self.rootdir = rootdir
        self.fileHashDir = rootdir + "\\.hash"
        self.noError = True
        self.readSize = 114514


    def CheckFileStatus( self, file ):
        if Path( file ).is_dir():
            return
        
        print( "Checking " +  file, end = "\t" )
        
        # Read file content and calc the hash
        fileHash = hashlib.md5()
        fileObject = open( file, "rb" )
        while True:
            fileContent = fileObject.read( self.readSize )
            if not fileContent:
                break
            fileHash.update( fileContent )
        fileObject.close()
        fileHash = fileHash.hexdigest()

        # Read hashfile content
        hashfilePath = self.fileHashDir + "\\" + os.path.split(file)[1] + ".md5"
        try:
            hashFile = open( hashfilePath, "r" )
            hashFileContent = hashFile.read()
        except OSError:
            print("Hashfile not found!")
            return
        
        # Compare file hash
        if fileHash == hashFileContent:
            print( "Succeeded!" )
        else:
            print( "Failed!" )
            self.noError = False
        return


    def CheckEachFile( self, path: str ):
        for dir in os.listdir( path ):
            currentPath = os.path.join( path, dir )
            if os.path.isdir( currentPath ) and os.path.split( currentPath )[1] != ".hash":
                self.CheckEachFile( currentPath )
            self.CheckFileStatus( currentPath )
            if self.noError == False:
                sys.exit( 1 )
    

    def WriteFileHash( self, file: str ):
        if Path( file ).is_dir():
            return
        
        print( "Calculating " +  file, end = "\t" )

        fileObject = open( file, "rb" )
        fileHash = hashlib.md5()
        while True:
            fileContent = fileObject.read( self.readSize )  # Prevent memory overflow
            if not fileContent:
                break
            fileHash.update( fileContent )
        fileObject.close()
        fileHash = fileHash.hexdigest()

        if not os.path.exists( self.fileHashDir ):
            os.mkdir( self.fileHashDir )
        hashFilePath = self.fileHashDir + "\\" + os.path.split(file)[1] + ".md5"
        hashFileObject = open( hashFilePath, "w" )
        hashFileObject.write( fileHash )
        hashFileObject.close()

        print( "Succeeded!" )
    

    def CalcEachFile( self, path: str ):
        for dir in os.listdir( path ):
            currentPath = os.path.join( path, dir )
            if os.path.isdir( currentPath ):
                self.CalcEachFile( currentPath )
            self.WriteFileHash( currentPath )


def main():
    parser = ArgumentParser()
    parser.add_argument( "action" )
    parser.add_argument( "rootpath" )
    args = parser.parse_args()
    
    hashClassObject = FileHash( args.rootpath )
    if args.action == "calc":
        hashClassObject.CalcEachFile( hashClassObject.rootdir )
    elif args.action == "check":
        hashClassObject.CheckEachFile( hashClassObject.rootdir )
        if hashClassObject.noError == True:
            print( "\nOK, No errors found." )
    else:
        print( "Actions can only be \"calc\" or \"check\"!" )

if __name__ == "__main__":
    main()
