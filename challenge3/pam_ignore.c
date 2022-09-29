/*Define which PAM interfaces we provice*/
#define PAM_SM_ACCOUNT
#define PAM_SM_AUTH
#define PAM_SM_PASSWORD
#define PAM_SM_SESSION

/*Include PAM headers*/
#include <security/pam_appl.h>
#include <security/pam_modules.h>

/*PAM entry point for session creation*/
int pam_sm_open_session(pam_handle_t *pamh, int flags, int argc, const char **argv){
	return(PAM_IGNORE);
}

int pam_sm_close_session(pam_handle_t *pamh, int flags, int argc, const char **argv){
	return(PAM_IGNORE);
}

int pam_sm_acct_mgmt(pam_handle_t *pamh, int flags, int argc, const char **argv){
	return(PAM_IGNORE);
}
