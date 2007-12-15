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
#include <unistd.h> 
#include <signal.h>
#include <dirent.h>
              
#include "ghttpd.h"

extern char assocNames[][2][100];

int serveconnection(int sockfd)
{
	FILE *in;
	char tempdata[8192], *ptr, *ptr2, *host_ptr1, *host_ptr2;
	char tempstring[8192], mimetype[50];
	char filename[255];
	unsigned int loop=0, flag=0;
	int numbytes=0;
	struct sockaddr_in sa;
	int addrlen = sizeof(struct sockaddr_in);
	t_vhost *thehost;
	
	thehost = &defaulthost;

// tempdata is the full header, tempstring is just the command

	while(!strstr(tempdata, "\r\n\r\n") && !strstr(tempdata, "\n\n"))
	{	
		if((numbytes=recv(sockfd, tempdata+numbytes, 4096-numbytes, 0))==-1)
			return -1;
	}
	for(loop=0; loop<4096 && tempdata[loop]!='\n' && tempdata[loop]!='\r'; loop++)
		tempstring[loop] = tempdata[loop];
	
	tempstring[loop] = '\0';
	ptr = strtok(tempstring, " ");
	if(ptr == 0) return -1;
	if(strcmp(ptr, "GET")) 
	{
		strcpy(filename, SERVERROOT);
		strcat(filename, "/cmderror.html");
		goto sendpage;
	}
	ptr = strtok(NULL, " ");
	if(ptr == NULL)
	{
		strcpy(filename, SERVERROOT);
		strcat(filename, "/cmderror.html");
		goto sendpage;
	}

	host_ptr1 = strstr(tempdata, "Host:");
	if(host_ptr1)
	{
		host_ptr2 = strtok(host_ptr1+6, " \r\n\t");
		
		for(loop=0; loop<no_vhosts; loop++)
			if(!gstricmp(vhosts[loop].host, host_ptr2))
				thehost = &vhosts[loop];
	}	
	else
		thehost = &defaulthost;
	if(strstr(ptr, "/.."))
	{
		strcpy(filename, SERVERROOT);
		strcat(filename, "/404.html");
		goto sendpage;
	}

	getpeername(sockfd, (struct sockaddr *)&sa, &addrlen);
	Log("Connection from %s, request = \"GET %s\"", inet_ntoa(sa.sin_addr), ptr);

	if(!strncmp(ptr, thehost->CGIBINDIR, strlen(thehost->CGIBINDIR)))
	{/* Trying to execute a cgi-bin file ? lets check */
		ptr2 = strstr(ptr, "?");
		if(ptr2!=NULL) { ptr2[0] = '\0'; flag = 1; }

		strcpy(filename, thehost->CGIBINROOT);
		ptr += strlen(thehost->CGIBINDIR);
		strcat(filename, ptr);

		// Filename = program to execute
		// ptr = filename in cgi-bin dir
		// ptr2+1 = parameters

		if(does_file_exist(filename)==TRUE && isDirectory(filename)==FALSE)
		{
			if(send(sockfd, "HTTP/1.1 200 OK\n", 16, 0)==-1)
			{
				fclose(in);
				return -1;
			}
			if(send(sockfd, "Server: "SERVERNAME"\n", strlen("Server: "SERVERNAME"\n"), 0)==-1)
			{
				fclose(in);
				return -1;
			}
			
			// Is a CGI-program that needs executing
			if(0 != dup2(sockfd, 0) || 1 != dup2(sockfd, 1))
				return -1;

			setbuf(stdin, 0);
			setbuf(stdout, 0);
			if(flag==1) setenv("QUERY_STRING", ptr2+1, 1);
			
			chdir(thehost->CGIBINROOT);
			
			execl(filename, "");
		}
		strcpy(filename, SERVERROOT);
		strcat(filename, "/cgierror.html");
		goto sendpage;
	}	

	strcpy(filename, thehost->DOCUMENTROOT);
	strcat(filename, ptr);
	      
	if(does_file_exist(filename)==FALSE)
	{		
		if(filename[strlen(filename)-1] == '/')
			strcat(filename, thehost->DEFAULTPAGE);
		else
		{
			strcat(filename, "/");
			strcat(filename, thehost->DEFAULTPAGE);
		}
		if(does_file_exist(filename) == FALSE)
		{
			filename[strlen(filename)-strlen(thehost->DEFAULTPAGE)-1] = '\0'; // Get rid of the /index.. 
			if(isDirectory(filename) == TRUE) { showdir(filename, sockfd, thehost); return 0; }
	
			// File does not exist, so we need to display the 404 error page..
			strcpy(filename, SERVERROOT);
			strcat(filename, "/404.html");
		}	
	
	}
sendpage:
	if((in = fopen(filename, "rb"))==NULL)
		return -1;
	
	fseek(in, 0, SEEK_END);
	
	if(send(sockfd, "HTTP/1.1 200 OK\n", 16, 0)==-1)
	{
		fclose(in);
		return -1;
	}
	if(send(sockfd, "Server: "SERVERNAME"\n", strlen("Server: "SERVERNAME"\n"), 0)==-1)
	{
		fclose(in);
		return -1;
	}
	sprintf(tempstring, "Content-Length: %d\n", ftell(in));
	if(send(sockfd, tempstring, strlen(tempstring), 0)==-1)
	{
		fclose(in);
		return -1;
	}

	getmimetype(filename, mimetype);
	sprintf(tempstring, "Content-Type: %s\n\n", mimetype);
	if(send(sockfd, tempstring, strlen(tempstring), 0)==-1)
	{
		fclose(in);
		return -1;
	}
	
	fseek(in, 0, SEEK_SET);

	while(!feof(in))
	{
		numbytes = fread(tempdata, 1, 1024, in);
		if(send(sockfd, tempdata, numbytes, 0)==-1)
		{
			fclose(in);
			return -1;
		}
	}
	fclose(in);

	close(sockfd);	
	return 0;
}

void getmimetype(char *filename, char *mimetype)
{
	char tempstring[50];
	char tempstring2[50];
	unsigned int loop=0;

	memset(tempstring, 0, 50);
	
	// Extract extension (will be reversed)
	for(loop=1; loop<strlen(filename) && filename[strlen(filename)-loop]!='.'; loop++)	
		tempstring[loop-1] = filename[strlen(filename)-loop];

	// Now we need to put the string around the right way..
	for(loop=0; loop<strlen(tempstring); loop++)
		tempstring2[loop] = tempstring[strlen(tempstring)-loop-1];
	
	tempstring2[loop] = '\0';
	
	// tempstring2 now contains the extension of the file, we now need
	// to search for the mimetype of the file

	for(loop=0; strcmp(assocNames[loop][0], "") && strcmp(assocNames[loop][0], tempstring2); loop++);

	strcpy(mimetype, assocNames[loop][1]);	
	if(!strcmp(mimetype, "")) strcpy(mimetype, "application/octet-stream");
}

void showdir(char *directory, int sockfd, t_vhost *thehost)
{
	struct dirent **namelist;
	int n, loop;
	unsigned long size=0;
	FILE *in;
	char tempstring[255];
	char dirheader[2048]; 
	const char dirfooter[] = "</TABLE><hr><center><font size=-1>This page is being provided to you by ghttpd<br><A HREF=\"http://members.xoom.com/gaztek\">http://members.xoom.com/gaztek</a></TD></TR></TABLE></BODY></HTML>\n";

	memset(dirheader, 0, 2048);

	sprintf(dirheader, "HTTP/1.1 200 OK\nServer: "SERVERNAME"\nContent-Type: text/html\n\n<HTML><BODY bgcolor=\"#33CCFF\"><center><TABLE BORDER=3 COLS=1 WIDTH=\"75%\" BGCOLOR=\"#66FFFF\"><tr><td><center><h2><u>Directory listing for %s</u></h2></center><TABLE BORDER=3 COLS=2 WIDTH=100% BGCOLOR=\"#FFFFFF\"><tr><td><b><center>Filename</center></b></td><td><b><center>Size (bytes)</center></b></td></tr>", directory+strlen(thehost->DOCUMENTROOT));

	if(send(sockfd, dirheader, sizeof(dirheader), 0) == -1)
		return;

	n = scandir(directory, &namelist, 0, alphasort);
	
	directory += strlen(thehost->DOCUMENTROOT);
	
	if (n < 0)
    		perror("scandir");
	else	
    		for(loop=0; loop<n; loop++) 
    		{
    			sprintf(tempstring, "%s%s/%s", thehost->DOCUMENTROOT, directory, namelist[loop]->d_name);
			size = get_file_size(tempstring);
			if(isDirectory(tempstring)) size=0;
    			sprintf(tempstring, "<tr><td><center><A HREF=\"%s/%s\">%s</a></center></td><td><center>%d</center></td></tr>\n", directory,namelist[loop]->d_name, namelist[loop]->d_name, size);
    			if(send(sockfd, tempstring, strlen(tempstring), 0)==-1)
    				return;
    		}

	send(sockfd, dirfooter, sizeof(dirfooter), 0);
}

char assocNames[][2][100] =
{
	{ "mp2", "audio/x-mpeg" },
	{ "mpa", "audio/x-mpeg" },
	{ "abs", "audio/x-mpeg" },
	{ "mpega", "audio/x-mpeg" },
	{ "mpeg", "video/mpeg" },
	{ "mpg", "video/mpeg" },
	{ "mpe", "video/mpeg" },
	{ "mpv", "video/mpeg" },
	{ "vbs", "video/mpeg" },
	{ "mpegv", "video/mpeg" },
	{ "bin", "application/octet-stream" },
	{ "com", "application/octet-stream" },
	{ "dll", "application/octet-stream" },
	{ "bmp", "image/x-MS-bmp" },
	{ "exe", "application/octet-stream" },
	{ "mid", "audio/x-midi" },
	{ "midi", "audio/x-midi" },
	{ "htm", "text/html" },
	{ "html", "text/html" },
	{ "txt", "text/plain" },
	{ "gif", "image/gif" },
	{ "tar", "application/x-tar" },
	{ "jpg", "image/jpeg" },
	{ "jpeg", "image/jpeg" },
	{ "png", "image/png" },
	{ "ra", "audio/x-pn-realaudio" },
	{ "ram", "audio/x-pn-realaudio" },
	{ "sys", "application/octet-stream" },
	{ "wav", "audio/x-wav" },
	{ "xbm", "image/x-xbitmap" },
	{ "zip", "application/x-zip" },
	{ "", "" }
};
