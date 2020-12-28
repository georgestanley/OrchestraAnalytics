select * from programs_temp where dirigent in ('György Cziffra d.J.', 'György Csiffra jun', 'IK');
select * from programs_temp where dirigent like '%Csiffra%';


--Spelling mistakes correction
update programs_temp set dirigent =  'Leopold Ludwig' where dirigent='LL';
update programs_temp set dirigent =  'Fritz Rieger' where dirigent='FR';
update programs_temp set dirigent =  'István Kertész' where dirigent='IK';
update programs_temp set dirigent =  'Marek Janowski' where dirigent='Janowski';
update programs_temp set dirigent =  'Ferdinand Leitner' where dirigent='FL';
update programs_temp set dirigent =  'Herbert Blomstedt' where dirigent='HB';
update programs_temp set dirigent =  'Bernhard Klee' where dirigent='Klee';
update programs_temp set dirigent =  'Moshe Atzmon' where dirigent='Moshe Moshe Atzmon';
update programs_temp set dirigent =  'Riccardo Chailly' where dirigent='Chailly';
update programs_temp set dirigent =  'György Cziffra' where dirigent='Györgi Csiffra jun.';
update programs_temp set dirigent =  'György Cziffra' where dirigent='György Cziffra d.J.';
update programs_temp set dirigent =  'Rafael Kubelík' where dirigent='Kubelik';
update programs_temp set dirigent =  'Wilhelm Österreicher' where dirigent='Wilheln Österreicher';
update programs_temp set dirigent =  'Wolfgang Sawallisch' where dirigent='Sawallisch';

update conductors set conductor =  'Leopold Ludwig' where conductor='LL';
update conductors set conductor =  'Fritz Rieger' where conductor='FR';
update conductors set conductor =  'István Kertész' where conductor='IK';
update conductors set conductor =  'Marek Janowski' where conductor='Janowski';
update conductors set conductor =  'Ferdinand Leitner' where conductor='FL';
update conductors set conductor =  'Herbert Blomstedt' where conductor='HB';
update conductors set conductor =  'Bernhard Klee' where conductor='Klee';
update conductors set conductor =  'Moshe Atzmon' where conductor='Moshe Moshe Atzmon';
update conductors set conductor =  'Riccardo Chailly' where conductor='Chailly';
update conductors set conductor =  'György Cziffra' where conductor='Györgi Csiffra jun.';
update conductors set conductor =  'György Cziffra' where conductor='György Cziffra d.J.';
update conductors set conductor =  'Rafael Kubelík' where conductor='Kubelik';
update conductors set conductor =  'Wilhelm Österreicher' where conductor='Wilheln Österreicher';
update conductors set conductor =  'Wolfgang Sawallisch' where conductor='Sawallisch';




