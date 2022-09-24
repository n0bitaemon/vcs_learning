#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <pwd.h>
#include <shadow.h>
#include <crypt.h>
#include <stdlib.h>
#include <sys/stat.h>

#define _PATH_SHADOW "/etc/shadow"
#define _PATH_SHADOW_BACKUP "/etc/shadow_backup"
#define _PATH_SHADOW_TEMP "/tmp/.shadow_temp"

int main(){
	FILE *fp_read = NULL, *fp_write = NULL;
	struct spwd *sp = NULL, *sp_entry = NULL;
	struct passwd *p = NULL;
	struct stat st_shadow;
	char *old_pwd = NULL, *new_pwd = NULL, *re_pwd = NULL, *encrypted = NULL;

	p = getpwuid(getuid());
	if(p->pw_name == NULL){
		printf("User %s does not exist\n", p->pw_name);
		exit(1);
	}

	sp_entry = getspnam(p->pw_name);
	old_pwd = strdup(getpass("Old password: "));
	encrypted = crypt(old_pwd, sp_entry->sp_pwdp);
	if(strcmp(encrypted, sp_entry->sp_pwdp) != 0){
		printf("mypasswd: incorrect password\n");
		printf("mypasswd: password unchanged\n");
		exit(2);
	}
	new_pwd = strdup(getpass("New password: "));
	re_pwd = strdup(getpass("Retype password: "));
	if(strcmp(new_pwd, re_pwd) != 0){
		printf("mypasswd: Sorry, passwords do not match\n");
		exit(3);
	}else if(strcmp(new_pwd, "") == 0){
		printf("password cannot be empty\n");
		exit(4);
	}else if(strcmp(new_pwd, my_pwd) == 0){
		printf("same password, password unchanged\n");
		exit(5);
	}

	if(!(fp_read = fopen(_PATH_SHADOW, "r")) 
		|| !(fp_write = fopen(_PATH_SHADOW_TEMP, "w"))){
		printf("an error occured, try again\n");
		exit(6);
	}

	while((sp = fgetspent(fp_read)) != (struct spwd *)0){
		if(strcmp(sp_entry->sp_namp, sp->sp_namp) == 0 
			&& strcmp(sp_entry->sp_pwdp, sp->sp_pwdp) == 0)
			sp->sp_pwdp = crypt(new_pwd, sp_entry->sp_pwdp);
		putspent(sp, fp_write);
	}
	fclose(fp_read);
	fclose(fp_write);
	stat(_PATH_SHADOW, &st_shadow);
	if(chown(_PATH_SHADOW_TEMP, st_shadow.st_uid, st_shadow.st_gid) != 0
		|| chmod(_PATH_SHADOW_TEMP, st_shadow.st_mode) != 0){
		printf("an error occured, try again\n");
		exit(7);
	}

	if(rename(_PATH_SHADOW, _PATH_SHADOW_BACKUP) != 0 
		|| rename(_PATH_SHADOW_TEMP, _PATH_SHADOW) != 0){
		printf("an error occured, try again\n");
		exit(8);
	}

	printf("mypasswd: password updated successfully\n");
	return 0;
}
