# dsl-connecare

This project is the backend of Acadela DSL, which compiles the input Clinical Pathway (CP) code written in Acadela to an SACM-compatible JSON format.

# Configure paths to Python executable and the Acadela compiler.

To run the backend, first we need to configure the *path to python executable* and *path to the acadela python compiler* in the **config.js** file:

module.exports = {  
  pythonPath: "path\\to\\Python>=3.8\\executable", //// e.g.: "E:\\Software\\Python\\3.8\\python.exe"  
  acadelaBackEndPath: "path\\to\\acadela_backend\\python\\compiler" //// e.g.: "E:\\dev_environment\\acadela_backend\\acadela"  
};  

# Configure connection to SACM

In case you want to see the generated CP code in Acadela **without SACM**, then set the CONN_SOCIOCORTEX config variable to False in the acadela\\config\\general_config.py file.

Otherwise, if SACM is used as the e-health platform that executes CPs, then a few configurations are required:

1) Clone and install brach **sacm** of **sociocortex** at https://github.com/sebischair/sociocortex/tree/sacm as the User Management platform. Java 1.7 & MySQL 5.6 are required. Higher version of Java or MySQL are not compatible. If you use MySQL, configure the connection as follows in the platform/config/configuration.txt file:

store = mysql  
store.database = sociocortex  
store.user = mustermann  
store.password = ottto # if this user or password is invalid, create a new user in the MySQL Database  
store.host = localhost  
store.port = 3306  

2) Clone and install the **sacm** github repository, branch **Tri_sacm_sociocortex_auth** at https://github.com/sebischair/sacm. Note: You may want to install a local undockerized **sacm** application.
2) In the general_config.py file, if you run the SACM and Sociocortex **outside localhost**, then you need to change the URL where SACM or Sociocortex is located. If Acadela, SACM, and sociocortex all run in your localhost, no need to change these parameters.

# Install dependencies

cd /path/to/acadela_backend
npm install

# Run the Acadela backend

cd /path/to/acadela_backend
npm start
