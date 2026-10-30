\set ON_ERROR_STOP on
\getenv app_password POINT_APP_PASSWORD
CREATE ROLE point LOGIN PASSWORD :'app_password';
ALTER DATABASE point_dev OWNER TO point;
CREATE DATABASE point_test OWNER point;
