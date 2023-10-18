#include <pwd.h>
#include <grp.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(){
	int ngroups = 100; /*The maximum number of groups*/
	char user[32];
	struct passwd *p = NULL; /*User's information*/
	gid_t *groups = NULL;
	struct group *gr = NULL;

	printf("Input username: "); scanf("%s", user);
	p = getpwnam(user);
	if(p == NULL){
		printf("user not exist\n");
		exit(1);
	}
	
	/*Get basic information*/
	groups = malloc(ngroups * sizeof(gid_t));
	printf("-----Information for %s----- \n", user);
	printf("UID: %d\n", (int)p->pw_uid);
	printf("Home directory: %s\n", p->pw_dir);
	
	/*Get user's group list*/
	if(getgrouplist(user, p->pw_gid, groups, &ngroups) == -1){
	        printf("error while trying to get user groups\n");
		exit(2);
	}
	printf("User's groups: ");
	for(int i = 0; i < ngroups; i++){
	        gr = getgrgid(groups[i]);
	        if(gr != NULL)
	                printf("%s(%d) ", gr->gr_name, groups[i]);
	}
	printf("\n");
	exit(0);
}
