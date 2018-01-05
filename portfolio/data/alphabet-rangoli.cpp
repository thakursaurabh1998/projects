#include<iostream>
#include"number.h"
using namespace std;
int n=1;
int main()
{
	char alpha_array[]={'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'};
	int i=num_entry();
	if(i<1 || i>{
		return 1;
	}
	int totalRows=((i-1)*2)+1;
	int totalColumns=((i-1)*4)+1;
	int midColumn=totalRows;
	for(int row=1; row<=totalRows; row++){
		if (row<=(totalRows/2)+1){
			int print_column=midColumn+2-(row*2);
			int alpha=i-1;
			for(int column=1; column<=totalColumns; column++){
				if(!(column%2)){
					cout<<"-";
				}
				else{
					if(column==print_column && column<midColumn){
						cout << alpha_array[alpha];
						alpha--;
						print_column+=2;
					}
					else if(column==print_column && column>=midColumn && column<=(midColumn+2*(row-1))){
						cout << alpha_array[alpha];
						alpha++;
						print_column+=2;
					}
					else{
						cout<<"-";
					}
				}
			}
			cout << endl;
		}
		else{	
			int print_column=midColumn+2-((row-2*n)*2);
			int alpha=i-1;
			for(int column=1; column<=totalColumns; column++){
				if(!(column%2))\{
					cout<<"-";
				}
				else{
					if(column==print_column && column<midColumn){
						cout << alpha_array[alpha];
						alpha--;
						print_column+=2;
					}
					else if(column==print_column && column>=midColumn && column<=(midColumn+2*(row-1)-4*n)){
						cout << alpha_array[alpha];
						alpha++;
						print_column+=2;
					}
					else{
						cout<<"-";
					}
				}
				
			}
			n++;
			cout << endl;
		} 
	}
	cin>>n;
	//system("pause");
	return 0;
}
