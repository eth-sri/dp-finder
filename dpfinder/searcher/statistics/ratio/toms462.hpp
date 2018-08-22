void bivariate_normal_cdf_values ( int &n_data, double &x, double &y,
  double &r, double &fxy );
// REMOVED THE FOLLOWING LINE
// double bivnor ( double ah, double ak, double r );
// ADDED THE FOLLOWING LINE
extern "C" double bivnor ( double ah, double ak, double r );
double gauss ( double t );
double r8_abs ( double x );
double r8_max ( double x, double y );
double r8_min ( double x, double y );
void timestamp ( );
