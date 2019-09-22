Postgresql Database startup:

// Sign into root user
sudo su -
// Start up postgresql service
service postgresql start
 * Starting PostgreSQL 11 database server                                [ OK ] 

// Sign into postgres user
sudo su - postgres
// Login into psql
psql
// Connect to fantasy fitness database
\c fantasyfitness;
