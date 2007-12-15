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

#ifndef GHTTPD_INCLUDE
#define GHTTPD_INCLUDE

typedef struct
{
	char host[255];
	char DOCUMENTROOT[255];
	char DEFAULTPAGE[255];
	char CGIBINDIR[255];
	char CGIBINROOT[255];
} t_vhost;

int serveconnection(int sockfd);
int does_file_exist(char *filename);
void getmimetype(char *filename, char *mimetype);
int isDirectory(char *filename);
void showdir(char *directory, int sockfd, t_vhost *thehost);
void readinconfig();
void Log(char *format, ...);
void getfileline(char *line, FILE *in);
void gstrlwr(char *string);
unsigned long get_file_size(char *filename);

#define SERVERNAME "GazTek HTTP Daemon v1.4"
extern unsigned int SERVERPORT;    /* the port browsers will be connecting to */
#define BACKLOG 150     /* how many pending connections the queue will hold */
extern char SERVERROOT[255];
extern char SERVERTYPE[255];
extern unsigned long no_vhosts;
extern t_vhost *vhosts;
extern t_vhost defaulthost;

#define TRUE	1
#define FALSE	0

#endif