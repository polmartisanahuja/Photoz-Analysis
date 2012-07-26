#include "4z_histos_parameters.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

float mean(float histo[], int dim)
{

	//Declaring variables..........................
	int i;
	float sum_x, mu;
	
	sum_x=0;
	for(i=0; i<dim; i++)
	{
		sum_x+=histo[i];
	}
	
	mu=sum_x/dim;
	
	return mu;
}

float rms(float histo[], int dim)
{

	//Declaring variables..........................
	int i;
	float rms, sum_x, sum_x2, mu;
	
	sum_x=0;
	for(i=0; i<dim; i++)
	{
		sum_x+=histo[i];
	}
	
	sum_x2=0;
	mu=sum_x/dim;
	for(i=0; i<dim; i++)
	{
		sum_x2+=pow(histo[i]-mu,2);
	}
	
	rms=sqrt(sum_x2/dim);
	
	return rms;
}

float rmserror(float histo[], int dim)
{

	//Declaring variables..........................
	int i;
	float Err_rms, sum_x, sum_x2, sum_x4, mu, m2, m4, factor;
	
	sum_x=0;
	for(i=0; i<dim; i++)
	{
		sum_x+=histo[i];
	}
	
	sum_x2=0;
	sum_x4=0;
	mu=sum_x/dim;
	for(i=0; i<dim; i++)
	{
		sum_x2+=pow(histo[i]-mu,2);
		sum_x4+=pow(histo[i]-mu,4);
	}
	
	m2=sum_x2/dim;
	m4=sum_x4/dim;
	factor=(dim-3)/(dim-1);
	
	Err_rms=sqrt(m4-(factor*pow(sqrt(m2),4)))/(2*sqrt(dim)*sqrt(m2));
		
	return Err_rms;
}


