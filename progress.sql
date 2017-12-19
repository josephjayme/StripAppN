create table stripper (
   stripperid text PRIMARY KEY NOT NULL,
   status boolean,
   switchvalue boolean,
   owner text,
   lat real,
   lng real
);

create table factory (
   productno text PRIMARY KEY NOT NULL,
   accesscode int NOT NULL
);

create table userpass (
    username text primary key,
    password text,
    fname text,
    lname text
);

create or replace function signup(par_username text, par_password text, par_fname text, par_lname text) returns text as
$$
  declare
    loc_id text;
    loc_res text;
  begin
     select into loc_id username from userpass where username = par_username;
     if loc_id isnull then
       insert into userpass (username, password, fname, lname) values (par_username, par_password, par_fname, par_lname);
       loc_res = 'OK';
     else
       loc_res = 'ID EXIST';
     end if;
     return loc_res;
  end;
$$
 language 'plpgsql';
 -- select signup('lemniscates', 'Radian.0', 'Joseph', 'Jayme');

create or replace function login(par_username text, par_password text) returns text as
$$
  declare
    loc_id text;
    loc_res text;
  begin
     select into loc_id username from userpass where username = par_username and password = par_password;
     if loc_id isnull then
       loc_res = 'NOT EXIST';
     else
       loc_res = 'OK';
     end if;
     return loc_res;
  end;
$$
 language 'plpgsql';
 -- select login(lemniscates, Radian.0);

create or replace function register(par_stripperid text, par_code int, par_owner text) returns text as
$$
  declare
    loc_id text;
    loc_id2 text;
    loc_res text;
  begin
     select into loc_id productno from factory where productno = par_stripperid and accesscode = par_code;
     if loc_id isnull then
       loc_res = 'VALIDATION ERROR';
     else
       select into loc_id2 stripperid from stripper where stripperid = par_stripperid;
       if loc_id2 isnull then
            insert into stripper (stripperid, status, switchvalue, owner, lat, lng) values (par_stripperid, False, False, par_owner, 0, 0);
            loc_res = 'OK';
       else
            loc_res = 'HAS OWNER';
       end if;
     end if;
     return loc_res;
  end;
$$
 language 'plpgsql';
-- select register('Stripper-4A75', 62363, 'lemni');

create or replace function addproduct(par_productno text, par_accesscode int) returns text as
$$
  declare
    loc_id text;
    loc_res text;
  begin
     select into loc_id productno from factory where productno = par_productno;
     if loc_id isnull then
       insert into factory (productno, accesscode) values (par_productno, par_accesscode);
       loc_res = 'OK';
     else
       loc_res = 'ID EXIST';
     end if;
     return loc_res;
  end;
$$
 language 'plpgsql';
-- select addproduct('Stripper-4A75', 62363);

create or replace function toggleswitch(par_stripperid text, par_switchvalue boolean) returns text as
$$
  declare
    loc_id text;
    loc_status boolean;
    loc_res text;
  begin
     select into loc_id stripperid from stripper where stripperid = par_stripperid;
     if loc_id isnull then
       loc_res = 'NOT EXIST';
     else
        update stripper set switchvalue = par_switchvalue where stripperid = par_stripperid;
        loc_res = 'OK';
     end if;
     return loc_res;
  end;
$$
 language 'plpgsql';
 -- select toggleswitch('Sripper-4A30', False);

create or replace function unregister(par_stripperid text) returns text as
$$
  declare
    loc_id text;
    loc_res text;
  begin
     select into loc_id stripperid from stripper where stripperid = par_stripperid;
     if loc_id isnull then
       loc_res = 'NOT EXIST';
     else
        delete from stripper where stripperid = par_stripperid;
        loc_res = 'OK';
     end if;
     return loc_res;
  end;
$$
 language 'plpgsql';
-- select unregister('Stripper-4A30');

create or replace function getregistered(in par_user text, out text, out boolean, out boolean) returns setof record as
$$
   select stripperid, status, switchvalue from stripper where owner = par_user;
$$
 language 'sql';
--select * from getregistered();

create or replace function getfname(in par_user text, out text) returns text as
$$
   select fname from userpass where username = par_user;
$$
 language 'sql';
--select getfname('judy');
