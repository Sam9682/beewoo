sudo cp /home/samuel/ipligence-max.mysqldump.sql.gz ./
sudo gunzip ./ipligence-max.mysqldump.sql.gz
sudo rm ipligence-max.mysqldump2.sql
sudo touch ipligence-max.mysqldump2.sql
sudo chmod a+w ipligence-max.mysqldump2.sql
sudo chmod a+x ipligence-max.mysqldump2.sql
sed -n '/INSERT/p' ipligence-max.mysqldump.sql >ipligence-max.mysqldump2.sql
sudo rm ipligence-max.mysqldump3.sql
sudo touch ipligence-max.mysqldump3.sql
sudo chmod a+w ipligence-max.mysqldump3.sql
sudo chmod a+x ipligence-max.mysqldump3.sql
sed 's/),(/\n/g' ipligence-max.mysqldump2.sql >ipligence-max.mysqldump3.sql
sudo rm ipligence-max.mysqldump4.sql
sudo touch ipligence-max.mysqldump4.sql
sudo chmod a+w ipligence-max.mysqldump4.sql
sudo chmod a+x ipligence-max.mysqldump4.sql
sudo sed 's/INSERT INTO `ipligence2` VALUES (//g' ipligence-max.mysqldump3.sql >ipligence-max.mysqldump4.sql
sudo rm ipligence-max.mysqldump5.sql
sudo touch ipligence-max.mysqldump5.sql
sudo chmod a+w ipligence-max.mysqldump5.sql
sudo chmod a+x ipligence-max.mysqldump5.sql
sudo sed 's/);//g' ipligence-max.mysqldump4.sql >ipligence-max.mysqldump5.sql
sudo rm ipligence-max.mysqldump.sql
sudo rm ipligence-max.mysqldump2.sql
sudo rm ipligence-max.mysqldump3.sql
sudo rm ipligence-max.mysqldump4.sql
sudo touch ipligence-max.mysqldump.sql
sudo chmod a+w ipligence-max.mysqldump.sql
sudo chmod a+x ipligence-max.mysqldump.sql
sudo cat header.txt >ipligence-max.mysqldump.sql
sudo cat ipligence-max.mysqldump5.sql >>ipligence-max.mysqldump.sql
sudo rm ipligence-max.mysqldump5.sql
