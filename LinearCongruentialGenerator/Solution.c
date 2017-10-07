#include<stdio.h>
#include<math.h>
char guess[20]="\\newcommand{\\settitl";
int a,b,m;
int f=0;
int gcd( int a, int b )
{
  if ( a==0 ) return b;
  return gcd( b%a, a );
}
void divisors(int n, int max)
{	
   int i=1;
   while(i <= sqrt(n))
    {
        if(n%i==0) {
        	if(i>max)
            	printf("\n%d,",i);
            if (i != (n / i) && n/i>max) {
                printf("\n%d,",n/i);
            }
        } 

        i++;
    }
}

int findDet(int p,int q, int r, int s)
{
	int max,det;
	det = p*(r-s)-q*(q-r)+(q*s-r*r);
	return abs(det);
}
void findabm(int p,int q, int r, int s, int t)
{
	int max;
	int det1;
	det1=findDet(p,q,r,s);
	printf("\nDet1 = %d",det1);
	if(p>=q && p>=r && p>=s)
		max=p;
	else if(q>=p && q>=r && q>=s)
		max=q;
	else if(r>=p && r>=q && r>=s)
		max=r;
	else
		max=s;
	//printf("%d\n%d",max,det);
	//printf("\nDivisors");
	//M is a integral multiple of det.
	//divisors(det,max);
	printf("\nMAX = %d",max);
	int i=max+1;
   while(i <= det1)
    {
        if(det1%i==0) 
		{
            		//printf("\n%d,",i);
            		int j;
            		m=i;
					for(j=1;j<m;j++)
					{
						if( ((r-q)-(q-p)*j)%m ==0 )
						{
							a=j;
							//printf("\na = %d",j);
							break;
						}	
					}
					b=(q-a*p)%m;
					//printf("\nb= %d",(q-j*p)%m);
					if( t== (a*s+b)%m)
					{
						printf("\n%d %d %d",a,b,m);
						printf("\nSUCCESS!!");
						f=1;
						return;
					}
    	} 
        i++;
    }
}

void main()
{
	//printf("%d",sizeof(guess));
	//int p=1865,q=7648,r=825,s=2582;
	FILE *inp;
	inp=fopen("hw2.tex.enc","r");
	int l,i,o=0,j=0;
	char p[4],q[4],r[4],s[4],t[4];
	int pi, qi, ri, si, ti;
	int fsize;
	fseek(inp, 0L, SEEK_END);
	fsize = ftell(inp);
	while(o<fsize)
	{
		fseek(inp,o,0);
		l=o%4;
		j=0;
		if(l==0)
			j=0;
		else
		{
			while( l<4 )
			{
				fgetc(inp);
				l++;
				j++;
			}
		}	
		for(i=0;i<4;i++)
		{
  			p[i] = (fgetc(inp)^guess[j++]);
  			//printf("\np[i] = %c",p[i]);			
  		}
        for(i=0;i<4;i++)
		{
  			q[i] = (fgetc(inp)^guess[j++]);			
  		}
  		for(i=0;i<4;i++)
		{
  			r[i] = (fgetc(inp)^guess[j++]);
  		}
  		for(i=0;i<4;i++)
		{
  			s[i] = (fgetc(inp)^guess[j++]);		
  		}
		for(i=0;i<4;i++)
		{
  			t[i] = (fgetc(inp)^guess[j++]);		
  		}
		pi = *(int *)p;
  		qi = *(int *)q;
  		ri = *(int *)r;
  		si = *(int *)s;
  		ti = *(int *)t;
  		//printf("\n%d %d %d %d %d",pi, qi,ri,si,ti);
  		if(pi>0 && qi>0 && ri>0 && si>0 && ti>0)
			findabm(pi,qi,ri,si,ti);
	  	if(f)
	  		break;
	  	else
			o++;
	}
	fclose(inp);
}

