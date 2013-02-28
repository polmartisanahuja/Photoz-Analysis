#include "4z_histos_parameters.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

float bootstrapmean(float histo[], int dim, char folder_name[])
{

	//Declaring variables..........................
	int N, k, k_rand;
	float r, rms, moment, Moment, Err_Moment;
	char histo_name[50];
	
	TH1F *gr1=new TH1F("gr1", "", 70 , 0.2 , 0.9);
	for(k=0; k < dim; k++) //Loop to fill histogram
	{
		gr1.Fill(histo[k]);
	}
	Moment=gr1.GetMean();
	
	//Creating Dz histogram...........................................................................
	TH1F *gr2=new TH1F("gr2", "", 100 , -0.01 , 0.01);
	for(N=1; N <= 1000; N++) //Loop for the N=dim histograms
	{
		TH1F *gr1=new TH1F("gr1", "", 70 , 0.2 , 0.9);
		for(k=1; k <= dim; k++) //Loop for the k=dim random values of the histogram
		{
		
			r=1;
			while(r==1) r=(float)rand()/RAND_MAX;
			r=r*(dim+1);
			k_rand=(int)(r);
			//printf("k_rand=%d\n", k_rand);
			
			gr1.Fill(histo[k_rand]);
			//printf("k=%d\n",k);
		}
		moment=gr1.GetMean();
		delete gr1;
		
		gr2.Fill(moment-Moment);
		printf("N=%d moment=%f\n", N, moment);
	}
	
	Err_Moment=gr2.GetRMS();
	printf("\nErr_Moment=%f\n", Err_Moment);
	
	//Plot moment distribution.....................
	gr2.GetXaxis().CenterTitle();
	gr2.GetYaxis().CenterTitle();
		
	gr2.SetXTitle("#Moment_{bootrap}-#Moment");
	gr2.SetYTitle("counts");

	gr2.Draw();
	
	sprintf(histo_name,"%s/bootstrap_mean.pdf", folder_name);
	c1.Print(histo_name);
	
	delete gr2;
	
	return Err_Moment;
}

float bootstraprms(float histo[], int dim, char folder_name[])
{

	//Declaring variables..........................
	int N, k, k_rand;
	float r, rms, moment, Moment, Err_Moment;
	char histo_name[50];
	
	TH1F *gr1=new TH1F("gr1", "", 70 , 0.2 , 0.9);
	for(k=0; k < dim; k++) //Loop to fill histogram
	{
		gr1.Fill(histo[k]);
	}
	Moment=gr1.GetRMS();
	
	//Creating Dz histogram...........................................................................
	TH1F *gr2=new TH1F("gr2", "", 100 , -0.01 , 0.01);
	for(N=1; N <= 1000; N++) //Loop for the N=dim histograms
	{
		TH1F *gr1=new TH1F("gr1", "", 70 , 0.2 , 0.9);
		for(k=1; k <= dim; k++) //Loop for the k=dim random values of the histogram
		{
		
			r=1;
			while(r==1) r=(float)rand()/RAND_MAX;
			r=r*(dim+1);
			k_rand=(int)(r);
			//printf("k_rand=%d\n", k_rand);
			
			gr1.Fill(histo[k_rand]);
			//printf("k=%d\n",k);
		}
		moment=gr1.GetRMS();
		delete gr1;
		
		gr2.Fill(moment-Moment);
		printf("N=%d moment=%f\n", N, moment);
	}
	
	Err_Moment=gr2.GetRMS();
	printf("\nErr_Moment=%f\n", Err_Moment);
	
	//Plot moment distribution.....................
	gr2.GetXaxis().CenterTitle();
	gr2.GetYaxis().CenterTitle();
		
	gr2.SetXTitle("#Moment_{bootrap}-#Moment");
	gr2.SetYTitle("counts");

	gr2.Draw();
	sprintf(histo_name,"%s/bootstrap_rms.pdf", folder_name);
	c1.Print(histo_name);
	
	delete gr2;
	
	return Err_Moment;
}

float bootstrapskewness(float histo[], int dim, char folder_name[])
{

	//Declaring variables..........................
	int N, k, k_rand;
	float r, rms, moment, Moment, Err_Moment;
	char histo_name[50];
	
	TH1F *gr1=new TH1F("gr1", "", 70 , 0.2 , 0.9);
	for(k=0; k < dim; k++) //Loop to fill histogram
	{
		gr1.Fill(histo[k]);
	}
	Moment=gr1.GetSkewness();
	
	//Creating Dz histogram...........................................................................
	TH1F *gr2=new TH1F("gr2", "", 100 , -2 , 2);
	for(N=1; N <= 1000; N++) //Loop for the N=dim histograms
	{
		TH1F *gr1=new TH1F("gr1", "", 70 , 0.2 , 0.9);
		for(k=1; k <= dim; k++) //Loop for the k=dim random values of the histogram
		{
		
			r=1;
			while(r==1) r=(float)rand()/RAND_MAX;
			r=r*(dim+1);
			k_rand=(int)(r);
			//printf("k_rand=%d\n", k_rand);
			
			gr1.Fill(histo[k_rand]);
			//printf("k=%d\n",k);
		}
		moment=gr1.GetSkewness();
		delete gr1;
		
		gr2.Fill(moment-Moment);
		printf("N=%d moment=%f\n", N, moment);
	}
	
	Err_Moment=gr2.GetRMS();
	printf("\nErr_Moment=%f\n", Err_Moment);
	
	//Plot moment distribution.....................
	gr2.GetXaxis().CenterTitle();
	gr2.GetYaxis().CenterTitle();
		
	gr2.SetXTitle("#Moment_{bootrap}-#Moment");
	gr2.SetYTitle("counts");

	gr2.Draw();
	sprintf(histo_name,"%s/bootstrap_skewness.pdf", folder_name);
	c1.Print(histo_name);
	
	delete gr2;
	
	return Err_Moment;
}

float bootstrapkurtosis(float histo[], int dim, char folder_name[])
{

	//Declaring variables..........................
	int N, k, k_rand;
	float r, rms, moment, Moment, Err_Moment;
	char histo_name[50];
	
	TH1F *gr1=new TH1F("gr1", "", 70 , 0.2 , 0.9);
	for(k=0; k < dim; k++) //Loop to fill histogram
	{
		gr1.Fill(histo[k]);
	}
	Moment=gr1.GetKurtosis();
	
	//Creating Dz histogram...........................................................................
	TH1F *gr2=new TH1F("gr2", "", 100 , -10 , 10);
	for(N=1; N <= 1000; N++) //Loop for the N=dim histograms
	{
		TH1F *gr1=new TH1F("gr1", "", 70 , 0.2 , 0.9);
		for(k=1; k <= dim; k++) //Loop for the k=dim random values of the histogram
		{
		
			r=1;
			while(r==1) r=(float)rand()/RAND_MAX;
			r=r*(dim+1);
			k_rand=(int)(r);
			//printf("k_rand=%d\n", k_rand);
			
			gr1.Fill(histo[k_rand]);
			//printf("k=%d\n",k);
		}
		moment=gr1.GetKurtosis();
		delete gr1;
		
		gr2.Fill(moment-Moment);
		printf("N=%d moment=%f\n", N, moment);
	}
	
	Err_Moment=gr2.GetRMS();
	printf("\nErr_Moment=%f\n", Err_Moment);
	
	//Plot moment distribution.....................
	gr2.GetXaxis().CenterTitle();
	gr2.GetYaxis().CenterTitle();
		
	gr2.SetXTitle("#Moment_{bootrap}-#Moment");
	gr2.SetYTitle("counts");

	gr2.Draw();
	sprintf(histo_name,"%s/bootstrap_kurtosis.pdf", folder_name);
	c1.Print(histo_name);
	
	delete gr2;
	
	return Err_Moment;
}

  

