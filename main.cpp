#include <QStorageInfo>
#include <iostream>

using namespace QtCore;

void drive_detection()
{
    foreach (const auto QStorageInfo &storage, QStorageInfo::mountedVolumes())
    {
        if (storage.isValid() && storage.isReady())
        {
            if (!storage.isReadOnly() && !storage.isRoot())
            {
                int storageUsed = storage.bytesTotal() - storage.bytesFree();

                cout << "Detachable Storage Device Detected!\n";
                cout << "Device Name: " << storage.name() << endl;
                cout << "Device Path: " << storage.device() << endl;
                cout << "File System: " << storage.fileSystemType() << endl;
                if (storage.bytesTotal() == -1)
                {
                    cout << "Device Storage: INVALID\n";
                }
                else 
                {
                    cout << "Device Storage:\n";
                    cout << "\tTotal Storage: " << storage.bytesTotal() << endl;
                    cout << "\tAvailable Storage: " << storage.bytesFree() << endl;
                    cout << "\tUsed Storage: " << storageUsed << endl;
                }
            }
        }
    }
}

int main()
{
    cout << "-----Data Loss Prevention Prototype-----\n";
    drive_detection();
    cout << "-----------------ver 0.1----------------\n";

    return 0;
}