#!/bin/bash

##Check all packages in the config file(pkg.conf)
##Check OK, proceed
##Check Fail, Error & Exit

source ./pkg.conf
pkgdir=`pwd`
jdk_package=`ls jdk*.tar.gz`
tomcat_package=`ls apache-tomcat*.tar.gz`
mysql_package=`ls mysql*.tar.gz`

if [ ! -z "$jdk_package" ] && [ ! -z "$tomcat_package" ] && [ ! -z "$mysql_package" ]; then
  echo " "
  echo "******************************************************"
  echo "**  Please check whether following packages are OK  **"
  echo "******************************************************"
  echo "** PATH......"$pkgdir
  echo "** JDK......."$jdk_package
  echo "** TOMCAT...."$tomcat_package
  echo "** MYSQL....."$mysql_package
  echo "******************************************************"
  echo " "
fi

echo "Do you want to proceed?"
select yn in "Yes" "No"; do
  case $yn in
    Yes ) echo Install Going LaLaLa...; break;;
    No ) echo Bye; exit;
  esac
done

echo "******************************************************"
echo "**               Installing JDK                     **"
echo "******************************************************"

jdk_name=`tar -zxvf ${pkgdir}/${jdk_package} -C ${jdk} | head -1 | cut -f1 -d"/"`
tar -zxvf ${pkgdir}/${jdk_package} -C ${jdk} >> /dev/null
echo export JAVA_HOME=${jdk}/${jdk_name} >> /etc/profile
echo "export PATH=$PATH:$JAVA_HOME/bin" >> /etc/profile
echo "export JRE_HOME=$JAVA_HOME/jre" >> /etc/profile
echo "export CLASSPATH=.:$JAVA_HOME/lib/tools.jar:$JAVA_HOME/lib/rt.jar" >> /etc/profile

echo export JAVA_HOME=${jdk}/${jdk_name} >> ~/.bashrc
echo "export PATH=$PATH:$JAVA_HOME/bin" >> ~/.bashrc
echo "export JRE_HOME=$JAVA_HOME/jre" >> ~/.bashrc
echo "export CLASSPATH=.:$JAVA_HOME/lib/tools.jar:$JAVA_HOME/lib/rt.jar" >> ~/.bashrc

###TODO auto check java install
source /etc/profile
echo `which java`
echo `which javac`
echo `which javaws`

echo "******************************************************"
echo "**             Installing TOMCAT                    **"
echo "******************************************************"

tomcat_name=`tar -zxvf ${pkgdir}/${tomcat_package} -C ${tomcat} | head -1 | cut -f1 -d"/"`
tar -zxvf ${pkgdir}/${tomcat_package} -C ${tomcat} >> /dev/null

echo ${tomcat}/${tomcat_name}

###TODO set catalina_home
###TODO auto check tomcat installation

echo "******************************************************"
echo "**             Installing MYSQL                     **"
echo "******************************************************"

mysql_name=`tar -zxvf ${pkgdir}/${mysql_package} -C ${mysql} | head -1 | cut -f1 -d"/"`
tar -zxvf ${pkgdir}/${mysql_package} -C ${mysql} >> /dev/null
cd ${mysql}
ln -s ${mysql}/${mysql_name} mysql
useradd -r -M -s /sbin/nologin mysql
chown -R mysql.mysql ${mysql}/${mysql_name}
chown -R mysql.mysql ${mysql}/mysql
chgrp -R mysql ${mysql}/${mysql_name}

cd ${mysql}/mysql/
./bin/mysql_install_db --user=mysql --basedir=${mysql}/mysql/ --datadir=${mysql}/mysql/data/
cp -a ./support-files/my-default.cnf /etc/my.cnf
cp -a ./support-files/mysql.server /etc/init.d/mysqld
cd bin/
./mysqld_safe --user=mysql &
/etc/init.d/mysqld restart > /dev/null

service mysqld status

chkconfig --level 35 mysqld on
echo "export PATH=$PATH:"${mysql}"/mysql/bin" >> /etc/profile
source /etc/profile
cat /root/.mysql_secret

echo "******************************************************"
echo "**             Copying Smartbi                      **"
echo "******************************************************"

cp ${pkgdir}/smartbi.war ${tomcat}/${tomcat_name}/webapps
nohup sh ${tomcat}/${tomcat_name}/bin/startup.sh > /dev/null 2>&1 &

echo "Please check whether Smartbi is normally started.(via catalina.out)"
read -p "After checked press any key to proceed or CTRL+C to exit"
