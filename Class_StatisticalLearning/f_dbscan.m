  function [class,type]=dbscan(x,minPts,eps) 
% Function to cluster data with Density-Based Scan Algorithm with Noise (DBSCAN)
% Distance function: Euklidean
% -------------------------------------------------------------------------
% Input: 
% x - data set (m,n); m-objects, n-attributes
% minPts - number of objects in a neighborhood of an object (minimal number of objects considered as a cluster)
% eps - neighborhood radius
% -------------------------------------------------------------------------
% Output: 
% class - vector specifying assignment of the i-th object to a cluster (m,1)
% type - vector specifying type of the i-th object (core: 1, border: 0, outlier: -1)
% -------------------------------------------------------------------------

% Written 2004 by Michal Daszykowski, Department of Chemometrics, Institute of Chemistry, The University of Silesia, http://www.chemometria.us.edu.pl
% code 24.10.2013 from http://chemometria.us.edu.pl/download/DBSCAN.M

[m,n]=size(x);

x = [[1:m]' x];
[m,n] = size(x);
type = zeros(1,m);
no = 1;
touched = zeros(m,1);

for i = 1:m             % loop over all objects
    if touched(i) == 0; % if the object is not classified yet
       ob = x(i,:);
       D = f_dist_eu(ob(2:n),x(:,2:n));
       ind = find(D<=eps);
   
       if length(ind)>1 && length(ind)<minPts+1   % object is a border point   
          type(i) = 0;
          class(i) = 0;
       end
       
       if length(ind)==1 % object is a noise point
          type(i) = -1;
          class(i) = -1; 
          touched(i) = 1;
       end

       if length(ind)>= minPts+1;   % if the current object is a core object
          type(i) = 1;
          class(ind) = ones(length(ind),1)*max(no);
         
          while ~isempty(ind)
                ob = x(ind(1),:);
                touched(ind(1)) = 1;
                ind(1) = [];
                D = f_dist_eu(ob(2:n),x(:,2:n));
                i1 = find(D<=eps);
    
                if length(i1)>1
                   class(i1) = no;
                   if length(i1) >= minPts+1;
                      type(ob(1)) = 1;
                   else
                      type(ob(1)) = 0;
                   end

                   for i = 1:length(i1)
                       if touched(i1(i)) == 0
                          touched(i1(i)) = 1;
                          ind = [ind i1(i)];  
                          class(i1(i)) = no;
                       end                   
                   end
                end
          end
          no = no+1;
       end
   end
end

i1 = find(class == 0);
class(i1) = -1;
type(i1) = -1;


function [D] = f_dist_eu(i,x)
% Calculates the Euclidean distances between the i-th object and all objects in x	 
%								    
% Input: 
% i - an object (1,n)
% x - data matrix (m,n); m-objects, n-variables	    
%                                                                 
% Output: 
% D - Euclidean distance (m,1)

[m,n] = size(x);
D = sqrt(sum((((ones(m,1)*i)-x).^2)'));

if n == 1
   D = abs((ones(m,1)*i-x))';
end

