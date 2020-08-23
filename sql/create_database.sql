create table if not exists website(
  id serial,
  url varchar,
  primary key (id),
  unique(url)
);

create table if not exists website_mon(
  request_time timestamp,
  website_id int not null,
  elapsed int,
  http_status_code int,
  pattern_match boolean,
  foreign key (website_id) references website(id)
);
