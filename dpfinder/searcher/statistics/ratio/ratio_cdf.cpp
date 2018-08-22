// ==BEGIN LICENSE==
// 
// MIT License
// 
// Copyright (c) 2018 SRI Lab, ETH Zurich
// 
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
// 
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.
// 
// ==END LICENSE==


#include <iostream>
#include <math.h>
#include <boost/math/distributions/normal.hpp> // for normal_distribution
#include <dlfcn.h> // for loading shared library
#include "toms462.hpp"

using boost::math::normal; // typedef provides default type is double.

using namespace std;

typedef double numb;

// http://static.stevereads.com/papers_to_read/on_the_ratio_of_two_correlated_normal_random_variables.pdf -> page 3


// LOAD TOMS462 functions
#define STRINGIFY2(X) #X
#define STRINGIFY(X) STRINGIFY2(X)
typedef double (*bivnorlib_t)( double ah, double ak, double r );
double bivnor( double ah, double ak, double r ){
	void* lib = dlopen(STRINGIFY(MYPATH)"/libtoms462.so", RTLD_LAZY);
	bivnorlib_t bivnorlib = (bivnorlib_t)dlsym(lib, "bivnor" );
	double ret = bivnorlib(ah, ak, r);
	dlclose(lib);
	return ret;
}


// MY FUNCTIONS

numb a(numb w, numb sx, numb sy, numb rho){
	numb w2=w*w;
	numb sx2=sx*sx;
	numb sy2=sy*sy;
	return sqrt(w2/sx2-2*rho*w/(sx*sy)+1/sy2);
}

double b(double w, double mx, double my, double sx, double sy, double rho){
	double sx2=sx*sx;
	double sy2=sy*sy;
	return mx*w/sx2-rho*(mx+my*w)/(sx*sy)+my/sy2;
}

double c(double mx, double my, double sx, double sy, double rho){
	double mx2=mx*mx;
	double sx2=sx*sx;
	double my2=my*my;
	double sy2=sy*sy;
	return mx2/sx2-2*rho*mx*my/(sx*sy)+my2/sy2;
}

double d(double w, double mx, double my, double sx, double sy, double rho){
	double a_=a(w,sx,sy,rho);
	double a2=a_*a_;
	double b_=b(w,mx,my,sx,sy,rho);
	double b2=b_*b_;
	double c_=c(mx,my,sx,sy,rho);
	double rho2=rho*rho;
	return exp((b2-c_*a2)/(2*(1-rho2)*a2));
}

numb phi(numb x){
	normal s; // (default mean = zero, and standard deviation = unity)
	return cdf(s,x);
}

numb ratio_pdf(numb w, numb mx, numb my, numb sx, numb sy, numb rho){
	numb a_=a(w,sx,sy,rho);
	numb b_=b(w,mx,my,sx,sy,rho);
	numb c_=c(mx,my,sx,sy,rho);
	numb d_=d(w,mx,my,sx,sy,rho);
	
	numb a2=a_*a_;
	numb a3=a_*a_*a_;
	numb rho2=rho*rho;
	
	numb pi=M_PI;
	
	numb frac1=b_*d_/(sqrt(2*pi)*sx*sy*a3);
	numb arg1=b_/(sqrt(1-rho2)*a_);
	numb arg2=-b_/(sqrt(1-rho2)*a_);
	numb frac2=sqrt(1-rho2)/(pi*sx*sy*a2);
	numb e=exp(-c_/(2*(1-rho2)));
	
	return frac1*(phi(arg1)-phi(arg2))+frac2*e;
}

numb ratio_cdf(numb w, numb mx, numb my, numb sx, numb sy, numb rho){
	//cout << "Running ratio_cdf with " << w << "/" << mx << "/" << my << "/" << sx << "/" << sy << endl;

	numb a_=a(w,sx,sy,rho);

	numb h1=(mx-my*w)/(sx*sy*a_);
	numb k1=-my/sy;
	numb gamma=(sy*w-rho*sx)/(sx*sy*a_);
	//cout << "Running with " << h1 << "/" << k1 << "/" << gamma << endl;
	numb L1=bivnor(h1,k1,gamma);
	
	numb h2=(my*w-mx)/(sx*sy*a_);
	numb k2=my/sy;
	//cout << "Running with " << h2 << "/" << k2 << "/" << gamma << endl;
	numb L2=bivnor(h2,k2,gamma);
	
	numb ret=L1+L2;
	return ret;
}

double ratio_cdf(double lower, double upper, double mx, double my, double sx, double sy, double rho){
	//mpf_set_default_prec(n_bits);
	
	numb lower_=lower;
	numb upper_=upper;
	numb mx_=mx;
	numb my_=my;
	numb sx_=sx;
	numb sy_=sy;
	numb rho_=rho;
	
	numb cdf1=ratio_cdf(upper_, mx_, my_, sx_, sy_, rho_);
	numb cdf2=ratio_cdf(lower_, mx_, my_, sx_, sy_, rho_);
	
	numb ret=cdf1-cdf2;
	return ret;//ret.get_d();
}

double interval_fallback_threshold=1e-7;

double get_err_interval(double p1,double p2,double std1,double std2,double center, double confidence){
	double confidence_2=1-(1-confidence)/2;
	double z_2=sqrt(2)*boost::math::erf_inv(confidence_2);
	double d1=std1*z_2;
	double d2=std2*z_2;
	if (p2>p1){
		swap(p1,p2);
		swap(d1,d2);
	}
	double err=0;
	if (p2-d2<=0){
		// p2 may be 0
		if (p2+d2<=0){
			// p2 must be 0. Thus, eps must be infinity
			err=0;
		}else{
			// p2 may or may not be 0. Thus, eps may or may not be infinity
			err=numeric_limits<double>::infinity();
		}
	}else if (p1-d1<=0){
			// p1 may be 0. In that case, eps would have to be -inf
			err=numeric_limits<double>::infinity();
	}else{
		// neither p1 nor p2 can be 0
		double min_eps=log(p1-d1)-log(p2+d2);
		double max_eps=log(p1+d1)-log(p2-d2);
		max_eps=max(max_eps,abs(min_eps));
		min_eps=max(min_eps,0.0);
		
		double eps=center;
		err=max(max_eps-eps,eps-min_eps);
	}
	return err;
}

// returns: confidence interval for logarithm of ratio
// center: center of confidence interval
// err_goal: precision of confidence interval
double ratio_confidence_interval(double p1, double p2, double d1, double d2, double corr, double center, double confidence, double err_goal){
	if (d1<interval_fallback_threshold || d2<interval_fallback_threshold){
			cout << "Falling back to interval arithmetic..." << endl;
			return get_err_interval(p1,p2,d1,d2,center,confidence);
	}
	
	double d_old=0;
	double d=err_goal/2;
	while (true) {
		double min=center-d;
		double max=center+d;
		double p=ratio_cdf(exp(min),exp(max),p1,p2,d1,d2,corr);
		//cout << "Pr[ratio∊ " << center << "±" << d << "]=" << p << " (exponential search)" << endl;
		if (p>=confidence){
			break;
		}
		d_old=d;
		d*=2;
		if (d>10){
			return INFINITY;
		}
	}
	double d_lower=d_old;
	double d_upper=d;
	while(d_upper-d_lower>err_goal/200){
		double middle=(d_lower+d_upper)/2;
		double min=center-middle;
		double max=center+middle;
		double p=ratio_cdf(exp(min),exp(max),p1,p2,d1,d2,corr);
		//cout << "Pr[ratio∊ " << center << "±" << middle << "]=" << p << " (binary search)" << endl;
		if (p<confidence){
			d_lower=middle;
		}else{
			d_upper=middle;
		}
	}
	
	/*double l=center-d_upper;
	double u=center+d_upper;
	double p_too_small=ratio_cdf(l,p1,p2,d1,d2,corr);
	double p_correct=ratio_cdf(l,u,p1,p2,d1,d2,corr);
	double p_too_large=1-ratio_cdf(u,p1,p2,d1,d2,corr);
	cout << "Pr[ratio<" << center << "-" << d_upper << "]=" << p_too_small << endl;
	cout << "Pr[ratio∊ " << center << "±" << d_upper << "]=" << p_correct << endl;
	cout << "Pr[ratio>" << center << "+" << d_upper << "]=" << p_too_large << endl;
	cout << p_too_small + p_correct + p_too_large << endl;*/
	
	return d_upper;
}

extern "C" {
	
	double ratio_cdf_extern(double lower, double upper, double mx, double my, double sx, double sy, double rho) {
		return ratio_cdf(lower,upper,mx,my,sx,sy,rho);
	}
	
	double ratio_pdf_extern(double w, double mx, double my, double sx, double sy, double rho) {
		return ratio_pdf(w,mx,my,sx,sy,rho);
	}
	
	double ratio_confidence_interval_extern(double p1, double p2, double d1, double d2, double corr, double center, double confidence, double err_goal){
		// cout << p1 << " " << p2 << " " << d1 << " " << d2 << " " << corr << " " << center << " " << confidence << " " << err_goal << endl;
		return ratio_confidence_interval(p1, p2, d1, d2, corr, center, confidence, err_goal);
	}

}


int main() {
	double x = bivnor(1,0,0);
	cout << x << endl;
	return 0;
}

