#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define REPORT_LENGTH 7

FILE *fp;

void execute(unsigned char bytes[REPORT_LENGTH]) {
    fwrite(bytes, 1, REPORT_LENGTH, fp);
}

int main(int argc, char* argv[]) {
    int i, num;

    int x = 0, y = 0, w = 0;
    int btn = 0;

    unsigned char bytes[REPORT_LENGTH];
    memset(bytes, 0, REPORT_LENGTH);

    fp = fopen("/dev/hidg0", "rb+");

    for (i = 1; i < argc; i++) {
        switch (argv[i][1]) {
            case 'b':
                i++;
                num = atoi(argv[i]);  
                bytes[0] |= 1 << (num - 1);
                break;
            case 'x':
                i++;
                x = atoi(argv[i]);
                bytes[1] = 0xff & x;
                bytes[2] = 0xff & (x >> 8);
                break;
            case 'y':
                i++;
                y = atoi(argv[i]);
                bytes[3] = 0xff & y;
                bytes[4] = 0xff & (y >> 8);
                break;
	    case 'w':
		i++;
		w = atoi(argv[i]);
		bytes[5] = 0xff & w;
		break;
        }
    }

    for (i = 0; i < 6; i++) {
        printf("\\\\x%x", bytes[i]);
    }
    printf("\n");

    execute(bytes);
    memset(bytes, 0, REPORT_LENGTH);

    execute(bytes);
}