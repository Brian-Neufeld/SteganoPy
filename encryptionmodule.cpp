#include <Windows.h>
#include <cmath>
#include <pybind11/pybind11.h>
#include <string>
#include <bitset>
#include <iostream>
#include <algorithm>



namespace py = pybind11;

// arrays to store the subkeys
int keys[8];
int keys8bit[16];

// subsitution boxes and their inverses
int sbox[16][16] = {
        {205, 30, 131, 91, 49, 1, 147, 74, 165, 80, 100, 225, 228, 164, 218, 250},
        {64, 93, 88, 213, 105, 18, 68, 208, 104, 78, 70, 77, 10, 209, 99, 95},
        {234, 113, 11, 206, 203, 12, 47, 137, 112, 85, 246, 255, 188, 211, 90, 200},
        {133, 63, 220, 242, 207, 53, 13, 116, 162, 154, 216, 193, 73, 201, 52, 106},
        {79, 145, 23, 97, 28, 26, 163, 40, 254, 130, 235, 61, 27, 43, 247, 71},
        {62, 172, 19, 33, 231, 150, 9, 66, 121, 58, 161, 196, 248, 7, 57, 199},
        {253, 114, 59, 191, 8, 16, 22, 155, 169, 156, 142, 245, 86, 175, 29, 51},
        {152, 202, 20, 42, 187, 108, 84, 118, 157, 159, 244, 212, 238, 148, 102, 183},
        {197, 229, 126, 44, 5, 0, 189, 180, 76, 167, 227, 224, 237, 55, 125, 170},
        {151, 103, 179, 136, 138, 222, 4, 110, 89, 182, 146, 119, 92, 81, 135, 186},
        {50, 239, 153, 115, 82, 37, 190, 251, 233, 31, 56, 83, 241, 107, 111, 221},
        {230, 192, 223, 65, 184, 219, 252, 72, 35, 243, 75, 21, 32, 226, 160, 128},
        {198, 158, 123, 178, 117, 174, 41, 101, 215, 176, 232, 124, 144, 149, 166, 87},
        {24, 17, 177, 25, 120, 240, 210, 132, 3, 139, 204, 54, 129, 185, 122, 45},
        {39, 140, 171, 236, 134, 249, 15, 34, 214, 141, 60, 38, 46, 98, 6, 127},
        {69, 14, 194, 36, 173, 143, 181, 48, 109, 96, 2, 168, 67, 217, 195, 94}};

int sboxinv[16][16] = {
        {133, 5, 250, 216, 150, 132, 238, 93, 100, 86, 28, 34, 37, 54, 241, 230},
        {101, 209, 21, 82, 114, 187, 102, 66, 208, 211, 69, 76, 68, 110, 1, 169},
        {188, 83, 231, 184, 243, 165, 235, 224, 71, 198, 115, 77, 131, 223, 236, 38},
        {247, 4, 160, 111, 62, 53, 219, 141, 170, 94, 89, 98, 234, 75, 80, 49},
        {16, 179, 87, 252, 22, 240, 26, 79, 183, 60, 7, 186, 136, 27, 25, 64},
        {9, 157, 164, 171, 118, 41, 108, 207, 18, 152, 46, 3, 156, 17, 255, 31},
        {249, 67, 237, 30, 10, 199, 126, 145, 24, 20, 63, 173, 117, 248, 151, 174},
        {40, 33, 97, 163, 55, 196, 119, 155, 212, 88, 222, 194, 203, 142, 130, 239},
        {191, 220, 73, 2, 215, 48, 228, 158, 147, 39, 148, 217, 225, 233,106, 245},
        {204, 65, 154, 6, 125, 205, 85, 144, 112, 162, 57, 103, 105, 120, 193, 121},
        {190, 90, 56, 70, 13, 8, 206, 137, 251, 104, 143, 226, 81, 244, 197, 109},
        {201, 210, 195, 146, 135, 246, 153, 127, 180, 221, 159, 116, 44, 134, 166, 99},
        {177, 59, 242, 254, 91, 128, 192, 95, 47, 61, 113, 36, 218, 0, 35, 52},
        {23, 29, 214, 45, 123, 19, 232, 200, 58, 253, 14, 181, 50, 175, 149, 178},
        {139, 11, 189, 138, 12, 129, 176, 84, 202, 168, 32, 74, 227, 140, 124, 161},
        {213, 172, 51, 185, 122, 107, 42, 78, 92, 229, 15, 167, 182, 96, 72, 43}};

int sbox8bit[4][4] = {
        {8, 2, 3, 5},
        {7, 1, 12, 4},
        {10, 0, 9, 14},
        {15, 13, 11, 6} };

int sboxinv8bit[4][4] = {
        {9, 5, 1, 2},
        {7, 3, 15, 4},
        {0, 10, 8, 14},
        {6, 13, 11, 12} };

// how amny rounds of xoring and swaping the data goes through
int rounds = 32;

#define INT_BITS 8

// functions that rotate the bits of a number to the left or right
// eg. 140 as an 8 bit integer rotated twice to the left would be 50
// 0b10001100 -> 0b00110010
// the 4 bit versions have to use an array of characters as integers are stored as unsigned ints are 8 bits
int leftRotate(int n, unsigned int d)
{
    d = d % 8;
    return (n << d) | (n >> (INT_BITS - d));
}

int rightRotate(int n, unsigned int d)
{
    d = d % 8;
    return (n >> d) | (n << (INT_BITS - d));
}

int leftRotate4bits(int n, unsigned int d)
{   
    
    d = d % 4;

    int nout = n;

    if (d == 0) {
        int nout = n;
    }
    else {
        std::string n_as_char = std::bitset< 4 >(n).to_string();
        std::string n_new_order = "";

        for (int i = 0; i < d; i++)
        {
            n_new_order = n_as_char.substr(1, 3) + n_as_char.substr(0, 1);
        }

        int nout = stoi(n_new_order, 0, 2);
    }

    return nout;
}

int rightRotate4bits(int n, unsigned int d)
{
    d = d % 4;
    int nout = n;

    if (d == 0) {
        int nout = n;
    }
    else {
        std::string n_as_char = std::bitset< 4 >(n).to_string();
        std::string n_new_order = "";

        for (int i = 0; i < d; i++)
        {
            n_new_order = n_as_char.substr(3, 1) + n_as_char.substr(0, 3);
        }

        n = stoi(n_new_order, 0, 2);
    }
    return n;
}

// functions that take a key, an audio sample, and the index of the audio sample  
// and encrypt or decrypt it with a feistel cipher. 
int encrypt16bit(unsigned long long int key, int audio_sample, int x) {
    // converts key to a binary string
    std::string keystr = std::to_string(key);
    std::string keybinary = std::bitset< 64 >(key).to_string();

    // splits key into 8 8 bit key parts
    for (int i = 0; i < 8; i++) {
        std::string keypart = keybinary.substr(i*8, 8);
        keys[i] = stoi(keypart, 0, 2);
    }

    // converts audio sample to binary string
    unsigned short int audio_samplenormalized = audio_sample;
    std::string audiobinary = std::bitset< 16 >(audio_sample).to_string();

    // 4 integer words are created by spliting the audio binary string
    int w1 = stoi(audiobinary.substr(0, 4), 0, 2);
    int w2 = stoi(audiobinary.substr(4, 4), 0, 2);
    int w3 = stoi(audiobinary.substr(8, 4), 0, 2);
    int w4 = stoi(audiobinary.substr(12, 4), 0, 2);

    // the 4 integer words are used as indices in the substitution boxes to creat left and right initial integers
    int L0 = sbox[w1][w2];
    int R0 = sbox[w3][w4];

    

    // this is the main part of the cipher, a round key is created by left bit rotating one of the key parts
    // this new key is then xored with R0 and then with L0 and assigned to R1 while L1 is just equal to R2
    // this continues for a set number of rounds before the final stage occurs 
    for (int j = 0; j < rounds; j++) {
        int roundkey = leftRotate(keys[j % 8], (x % 8));
        int fint = R0 ^ roundkey;
        int R1 = L0 ^ fint;
        int L1 = R0;
        L0 = L1;
        R0 = R1;
        
    }

    // in the final ecryption stage, L and R are not swapped at the end
    int roundkey = leftRotate(keys[rounds % 8], (x % 8));
    int fint = R0 ^ roundkey;
    int L1 = L0 ^ fint;
    int R1 = R0;
    int Lout = L1;
    int Rout = R1;

    // L and R are now converted back to a binary string 
    std::string Loutstr = std::bitset< 8 >(Lout).to_string();
    std::string Routstr = std::bitset< 8 >(Rout).to_string();

    // the binary strings are then converted to an integer 
    int outaudio_sample = stoi(Loutstr + Routstr, 0, 2);

    return outaudio_sample;
}

int decrypt16bit(unsigned long long int key, int audio_sample, int x) {
    

    std::string keystr = std::to_string(key);
    std::string keybinary = std::bitset< 64 >(key).to_string();
    



    for (int i = 0; i < 8; i++) {
        std::string keypart = keybinary.substr(i * 8, 8);
        keys[i] = stoi(keypart, 0, 2);
    }


   int encodedaudio = audio_sample;


   std::string encodedbin = std::bitset< 16 >(encodedaudio).to_string();



   int L0 = stoi(encodedbin.substr(0, 8), 0, 2);
   int R0 = stoi(encodedbin.substr(8, 8), 0, 2);



   for (int j = 0; j < rounds; j++) {
       int roundkey = leftRotate(keys[(rounds-j) % 8], (x % 8));
       int fint = R0 ^ roundkey;
       int R1 = L0 ^ fint;
       int L1 = R0;
       L0 = L1;
       R0 = R1;

   }

   int roundkey = leftRotate(keys[0], (x % 8));
   int fint = R0 ^ roundkey;
   int L1 = L0 ^ fint;
   int R1 = R0;
   int Lout = L1;
   int Rout = R1;

   std::string Loutbin = std::bitset< 8 >(Lout).to_string();
   std::string Routbin = std::bitset< 8 >(Rout).to_string();



   int w1 = stoi(Loutbin.substr(0, 4), 0, 2);
   int w2 = stoi(Loutbin.substr(4, 4), 0, 2);
   int w3 = stoi(Routbin.substr(0, 4), 0, 2);
   int w4 = stoi(Routbin.substr(4, 4), 0, 2);

   int Loutsbox = sboxinv[w1][w2];
   int Routsbox = sboxinv[w3][w4];

   std::string Loutbin2 = std::bitset< 8 >(Loutsbox).to_string();
   std::string Routbin2 = std::bitset< 8 >(Routsbox).to_string();


   int outaudio_sampledecode = stoi(Loutbin2 + Routbin2, 0, 2);

    return outaudio_sampledecode;
}

int encrypt8bit(unsigned long long int key, int audio_sample, int x) {
    // converts key to a binary string
    std::string keystr = std::to_string(key);
    std::string keybinary = std::bitset< 64 >(key).to_string();

    // splits key into 16 4 bit key parts
    for (int i = 0; i < 16; i++) {
        std::string keypart = keybinary.substr(i * 4, 4);
        keys8bit[i] = stoi(keypart, 0, 2);
    }

    // converts audio sample to binary string
    unsigned int audio_samplenormalized = audio_sample;
    std::string audiobinary = std::bitset< 8 >(audio_sample).to_string();
    

    // 4 integer words are created by spliting the audio binary string
    int w1 = stoi(audiobinary.substr(0, 2), 0, 2);
    int w2 = stoi(audiobinary.substr(2, 2), 0, 2);
    int w3 = stoi(audiobinary.substr(4, 2), 0, 2);
    int w4 = stoi(audiobinary.substr(6, 2), 0, 2);

    // the 4 integer words are used as indices in the substitution boxes to creat left and right initial integers
    int L0 = sbox8bit[w1][w2];
    int R0 = sbox8bit[w3][w4];


    // this is the main part of the cipher, a round key is created by left bit rotating one of the key parts
    // this new key is then xored with R0 and then with L0 and assigned to R1 while L1 is just equal to R2
    // this continues for a set number of rounds before the final stage occurs 
  

    for (int j = 0; j < rounds; j++) {
        int roundkey = leftRotate4bits(keys8bit[j % 16], (x % 4));
        int fint = R0 ^ roundkey;
        int R1 = L0 ^ fint;
        int L1 = R0;
        L0 = L1;
        R0 = R1;
    }

    // in the final ecryption stage, L and R are not swapped at the end
    int roundkey = leftRotate4bits(keys8bit[rounds % 16], (x % 4));
    int fint = R0 ^ roundkey;
    int L1 = L0 ^ fint;
    int R1 = R0;
    int Lout = L1;
    int Rout = R1;

    // L and R are now converted back to a binary string 
    std::string Loutstr = std::bitset< 4 >(Lout).to_string();
    std::string Routstr = std::bitset< 4 >(Rout).to_string();

    // the binary strings are then converted to an integer 
    short int outaudio_sample = stoi(Loutstr + Routstr, 0, 2);

    return outaudio_sample;
}

int decrypt8bit(unsigned long long int key, int audio_sample, int x) {
  
    std::string keystr = std::to_string(key);
    std::string keybinary = std::bitset< 64 >(key).to_string();



    for (int i = 0; i < 16; i++) {
        std::string keypart = keybinary.substr(i * 4, 4);
        keys8bit[i] = stoi(keypart, 0, 2);
    }


    unsigned short int encodedaudio = audio_sample;

    std::string encodedbin = std::bitset< 8 >(encodedaudio).to_string();

    int L0 = stoi(encodedbin.substr(0, 4), 0, 2);
    int R0 = stoi(encodedbin.substr(4, 4), 0, 2);


    for (int j = 0; j < rounds; j++) {
        int roundkey = leftRotate4bits(keys8bit[(rounds - j) % 16], (x % 4));
        int fint = R0 ^ roundkey;
        int R1 = L0 ^ fint;
        int L1 = R0;
        L0 = L1;
        R0 = R1;
    }

    int roundkey = leftRotate4bits(keys[0], (x % 4));
    int fint = R0 ^ roundkey;
    int L1 = L0 ^ fint;
    int R1 = R0;
    int Lout = L1;
    int Rout = R1;

    


    std::string Loutbin = std::bitset< 4 >(Lout).to_string();
    std::string Routbin = std::bitset< 4 >(Rout).to_string();


    int w1 = stoi(Loutbin.substr(0, 2), 0, 2);
    int w2 = stoi(Loutbin.substr(2, 2), 0, 2);
    int w3 = stoi(Routbin.substr(0, 2), 0, 2);
    int w4 = stoi(Routbin.substr(2, 2), 0, 2);

    int Loutsbox = sboxinv8bit[w1][w2];
    int Routsbox = sboxinv8bit[w3][w4];

    std::string Loutbin2 = std::bitset< 4 >(Loutsbox).to_string();
    std::string Routbin2 = std::bitset< 4 >(Routsbox).to_string();


    short int outaudio_sampledecode = stoi(Loutbin2 + Routbin2, 0, 2);

    return outaudio_sampledecode;
}

PYBIND11_MODULE(encryptionmodule, m) {
    m.def("encrypt16bit", &encrypt16bit);
    m.def("decrypt16bit", &decrypt16bit);
    m.def("encrypt8bit", &encrypt8bit);
    m.def("decrypt8bit", &decrypt8bit);

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
