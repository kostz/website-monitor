create table website(
  id serial,
  url varchar,
  primary key (id),
  unique(url)
);

create table website_mon (
  time timestamp,
  website_id int not null,
  elapsed int,
  http_status_code int,
  pattern_match boolean,
  foreign key (website_id) references website(id) on delete cascade
);
