/*
GazTek HTTP Daemon (ghttpd)
Copyright (C) 1999  Gareth Owen <gaz@athene.co.uk>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
*/

#include <stdio.h> 
#include <stdlib.h> 
#include <errno.h> 
#include <string.h> 
#include <sys/types.h> 
#include <netinet/in.h> 
#include <sys/socket.h> 
#include <sys/wait.h> 
#include <sys/time.h> 
#include <sys/stat.h>
#include <unistd.h> 
#include <signal.h>
#include <ctype.h>
#include <dirent.h>
#include <stdarg.h>
              
#include "ghttpd.h"
int gstricmp(char *string1, char *string2);
void VirtualHostDefinition(FILE *in);

void getfileline(char *line, FILE *in)
{
	unsigned int loop=0;
	fgets(line, 255, in);
	for(loop=0; loop<255 && line[loop]!='\0'; loop++) if(line[loop]=='\r' || line[loop]=='\n') line[loop] = '\0';
}

int does_file_exist(char *filename)
{
	struct stat st;
	if(stat(filename, &st) || isDirectory(filename)) return FALSE;
	return TRUE;
}

unsigned long get_file_size(char *filename)
{
	struct stat st;
	if(!stat(filename, &st)) return st.st_size;
	return 0;
}

int isDirectory(char *filename)
{
	struct stat st;
	
	if(stat(filename, &st)) return FALSE;  // Doesnt exist
	if(!S_ISDIR(st.st_mode)) return FALSE; // Is not directory
	
	return TRUE;
}

unsigned long count_vhosts()
{
	FILE *in;
	unsigned long count=0;
	char tempstring[255], *ptr1=0;

	if((in = fopen("/etc/ghttpd.conf", "rt")) == NULL)
		return 0;
		
	while(!feof(in))
	{
		memset(tempstring, 0, 255);
		getfileline(tempstring, in);
		if(feof(in)) break;
		
		ptr1 = strtok(tempstring, " \t\n\r");
		if(ptr1 && !gstricmp(ptr1, "<virtualhost>"))
			count++;
	}

	fclose(in);
	return count;
}

void VirtualHostDefinition(FILE *in)
{
	char tempstring[255], *ptr1=0, *ptr2=0;
	t_vhost *thevhost=0;
	
	thevhost = &vhosts[no_vhosts];

	strcpy(thevhost->host, "");
	strcpy(thevhost->DOCUMENTROOT, defaulthost.DOCUMENTROOT);
	strcpy(thevhost->DEFAULTPAGE, defaulthost.DEFAULTPAGE);
	strcpy(thevhost->CGIBINDIR, defaulthost.CGIBINDIR);
	strcpy(thevhost->CGIBINROOT, defaulthost.CGIBINROOT);
	
	while(!feof(in))
	{
		getfileline(tempstring, in);

		if(feof(in)) break;
		ptr1 = strtok(tempstring, "\" \t");
		ptr2 = strtok(NULL, "\" \t");
	
		if(!ptr1) continue;
		if(ptr1[0]!='<' && !ptr2) continue;
		if(ptr1[0] == '#') continue; 

		if(!gstricmp(ptr1, "</virtualhost>"))
			break;
		else if(!gstricmp(ptr1, "Host"))
			strcpy(thevhost->host, ptr2);
		else if(!gstricmp(ptr1, "DocumentRoot"))
		        strcpy(thevhost->DOCUMENTROOT, ptr2);
		else if(!gstricmp(ptr1, "DefaultPage"))
		        strcpy(thevhost->DEFAULTPAGE, ptr2);
		else if(!gstricmp(ptr1, "CgiBinDir"))
		        strcpy(thevhost->CGIBINDIR, ptr2);
		else if(!gstricmp(ptr1, "CgiBinRoot"))
		        strcpy(thevhost->CGIBINROOT, ptr2);        
	}

	no_vhosts++;
}

void gstrlwr(char *string)
{
	unsigned int loop=0;
	
	if(!string) return;
	for(loop=0; loop<255 && string[loop]; loop++)
		string[loop] = tolower(string[loop]);
}

void readinconfig()
{
	FILE *in;
	char *ptr1=0, *ptr2=0;
	char tempstring[255];
	int loop=0;
	
	// If config file cannot be read then the defaults will be used
	if((in = fopen("/etc/ghttpd.conf", "rt"))==NULL)
		return;

	no_vhosts=0;

	while(!feof(in))
	{
		getfileline(tempstring, in);

		if(feof(in)) break;
		ptr1 = strtok(tempstring, "\"\t ");
		ptr2 = strtok(NULL, "\"\t ");
		
		if(!ptr1) continue;
		if(ptr1[0]!='<' && !ptr2) continue;
		if(ptr1[0] == '#') continue;
	
		if(!gstricmp(ptr1, "ServerRoot"))
			strcpy(SERVERROOT, ptr2);
		else if(!gstricmp(ptr1, "DocumentRoot"))
			strcpy(defaulthost.DOCUMENTROOT, ptr2);
		else if(!gstricmp(ptr1, "DefaultPage"))
			strcpy(defaulthost.DEFAULTPAGE, ptr2);
		else if(!gstricmp(ptr1, "CgiBinDir"))
			strcpy(defaulthost.CGIBINDIR, ptr2);
		else if(!gstricmp(ptr1, "CgiBinRoot"))
			strcpy(defaulthost.CGIBINROOT, ptr2);
		else if(!gstricmp(ptr1, "ServerPort"))
			SERVERPORT = atoi(ptr2);
		else if(!gstricmp(ptr1, "ServerType"))
			strcpy(SERVERTYPE, ptr2);
		else if(!gstricmp(ptr1, "<VirtualHost>"))
			VirtualHostDefinition(in);
		else
			printf("Warning: unknown variable in config file \"%s\"\n", ptr1);
	}
		
	fclose(in);
}

int gstricmp(char *string1, char *string2)
{
	int loop=0;
	
	if(!string1 || !string2) return 1;

	while(*string1 && *string2)
	if(tolower(*(string1++)) != tolower(*(string2++))) return 1;

	if(tolower(*(string1++)) != tolower(*(string2++))) return 1;

	return 0;
}

void Log(char *format, ...)
{
	FILE *logfile;
	time_t t;
	struct tm *tm;
	char temp[200], temp2[200], logfilename[255];
	char datetime[] = "[%d.%m.%Y] [%H:%M.%S]";
	char datetime_final[128];
	va_list ap;

	va_start(ap, format);		// format it all into temp
	vsprintf(temp, format, ap);
	va_end(ap);

	time (&t);
	tm = localtime(&t);
	memset(datetime_final, 0, 128);
	strftime(datetime_final, 127, datetime, tm);
	
	// format it all so we have date/time/loginfo
	sprintf(temp2, "%s - %s\n", datetime_final, temp);
	sprintf(logfilename, "%s/ghttpd.log", SERVERROOT);

	if((logfile = fopen(logfilename, "at"))==NULL)
		return;

	fputs(temp2, logfile);		// Save to the file
		
	fclose(logfile);		// Close file
}