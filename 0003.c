#include <stdlib.h>
#include <magic.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <signal.h>
#include <fcntl.h>

#define CONNMAX 1000
#define BYTES 1024

char *ROOT; // path to root of files served.
int listenfd, clients[ CONNMAX ];
void error( char* );
void startServer( char* );
void respond( int, magic_t );
volatile int sockio = -1, non = 0, clientn = -1, attn = 0;
FILE* sockbuf = NULL;
char recent[ 4096 ];

void io( int signal )
{
   fd_set inputs;
   FD_ZERO( &inputs );
   FD_SET( sockio, &inputs );
   if( sockio == -1 || clientn == -1 )
   {
      printf( "x" );
      fflush( stdout );
      sleep( 0.1 );
      return;
   }
   int count = 0;
   struct timeval time_zero = { 0, 0 };
//   printf( "*%d*", sockio );
   fflush( stdout );
   count = select( FD_SETSIZE, &inputs, NULL, NULL, &time_zero );
   while( count != 0 )
   {
      int rc;
      if( FD_ISSET( sockio, &inputs ) )
      {
         char inbuf;

//         for(;;)
         {
//            rc = fread( &inbuf, 1, 1, sockbuf );
            rc = recv( sockio, &inbuf, 1, 0 );
            if( inbuf == '\r' )
               ;//printf( "\r" );
            else if( inbuf == '\n' )
            {
               printf( "_\n" );
               send( clients[ clientn ], "\r\n", 2, 0 );
               attn = 0;
               if( non > 0 && non < 4 )
                  //printf( "re: ", recent );
                  recent[ attn ] = '\0';
               ++non;
            }
            else
            {
               send( clients[ clientn ], &inbuf, 1, 0 );
               printf( "%c_", inbuf );
               recent[ attn ] = inbuf;
               recent[ attn + 1 ] = '\0';
               ++attn;
//            break;
            }
         }
      }
      FD_ZERO( &inputs );
      FD_SET( sockio, &inputs );

      count = select( FD_SETSIZE, &inputs, NULL, NULL, &time_zero );
   }
   FD_ZERO( &inputs );
}

int main( int argc, char* argv[] )
{
   struct sockaddr_in clientaddr;
   socklen_t addrlen;
   char c;    
   magic_t sis;

   sis = magic_open( MAGIC_MIME_TYPE );
   magic_load( sis, "/usr/lib/file/magic.mgc" );

   // default Values ROOT = ./ and PORT=10000
   char PORT[6];
   ROOT = getenv( "PWD" );
   strcpy( PORT, "10000" );

   signal( SIGIO, io );

   int slot=0;

   printf( "Server started at port no. %s%s%s with root directory as %s%s%s\n", "\033[92m", PORT, "\033[0m", "\033[92m", ROOT, "\033[0m" );
   // Setting all elements to -1: signifies there is no client connected
   int i;
   for( i = 0; i < CONNMAX; ++i )
      clients[ i ]=-1;
   startServer( PORT );

   // ACCEPT connections
   for(;;)
   {
      addrlen = sizeof( clientaddr );
      clients[ slot ] = accept( listenfd, (struct sockaddr *) &clientaddr, &addrlen );

      if( clients[ slot ] < 0 )
         error( "accept() error" );
      else
      {
      	 if ( fork()==0 )
      	 {
	    respond(slot, sis);
	    exit(0);
	 }
      }
      while( clients[ slot ] != -1 )
      	slot = ( slot + 1 ) % CONNMAX;
   }

   magic_close( sis );
   return 0;
}

//start server
void startServer(char *port)
{
   struct addrinfo hints, *res, *p;

   // getaddrinfo for host
   memset( &hints, 0, sizeof( hints ) );
   hints.ai_family = AF_INET;
   hints.ai_socktype = SOCK_STREAM;
   hints.ai_flags = AI_PASSIVE;
   if( getaddrinfo( NULL, port, &hints, &res ) != 0 )
   {
      perror ("getaddrinfo() error");
      exit( EXIT_FAILURE );
   }
   // socket and bind
   for( p = res; p != NULL; p = p -> ai_next )
   {
      listenfd = socket( p -> ai_family, p -> ai_socktype, 0 );
      if( listenfd == -1 ) continue;
      if( bind( listenfd, p->ai_addr, p->ai_addrlen ) == 0 ) break;
   }
   if( p == NULL )
   {
      perror( "socket() or bind()" );
      exit( EXIT_FAILURE );
   }
   freeaddrinfo( res );

   // listen for incoming connections
   if( listen( listenfd, 1000000 ) != 0 )
   {
      perror( "listen() error" );
      exit( EXIT_FAILURE );
   }
}

//#include <stdio.h>
//#include <stdlib.h>
//#include <sys/socket.h>
//#include <netinet/in.h>
#include <netdb.h>

void init_sockaddr (struct sockaddr_in *name,
               const char *hostname,
               uint16_t port)
{
  struct hostent *hostinfo;

  name->sin_family = AF_INET;
  name->sin_port = htons (port);
  hostinfo = gethostbyname (hostname);
  if (hostinfo == NULL)
    {
      fprintf (stderr, "Unknown host %s.\n", hostname);
      exit (EXIT_FAILURE);
    }
  name->sin_addr = *(struct in_addr *) hostinfo->h_addr;
}

FILE* query( char* cx )
{
   struct sockaddr_in sender;
   struct sockaddr* a_sock = NULL;
   int sock, len_cx, flags = 0, err = 0;
   char* sis;
   FILE* boom;
   init_sockaddr( &sender, "127.0.0.1", 5001 );
   a_sock = malloc( sizeof( short int ) + sizeof( sender ) );
   a_sock -> sa_family = AF_INET;
   printf( "socket addr bytes: %d\n", sizeof( sender ) );
//   memcpy( a_sock -> sa_data, &sender, sizeof( sender ) ); // 14 bytes max
   memcpy( a_sock, &sender, sizeof( sender ) ); // 14 bytes max
   sock = socket( PF_INET, SOCK_STREAM, 0 );
   len_cx = strlen( cx + 1 ) + 1; // '\n'
//   len_cx = strlen( cx + 1 ) + 2; // '\n'
   sis = malloc( len_cx );
   strcpy( sis, cx + 1 );
   strcat( sis, "\n" );
//   strcat( sis, "\r\n" );
//   printf( "connect\n" );
   err = connect( sock, a_sock, sizeof( sender ) );
//   err = connect( sock, a_sock, sizeof( short int ) + sizeof( sender ) );
//   printf( "err: %d", err );
   if( err == -1 );
//      perror( "error" );
   boom = fdopen( sock, "rw" );
   sockbuf = boom;
   flags = fcntl( sock, F_GETFL, 0 );
   if( flags == -1 ) printf( "bad flags.\n" );
   fcntl( sock, F_SETFL, flags | O_ASYNC | O_NONBLOCK );
   fcntl( sock, F_SETOWN, getpid() );
//   signal( SIGIO, io );
//   sleep( 1 );
   sockio = sock;
//   printf( "get\n" );
//   send( sock, "get\n", 4, 0 );
   send( sock, "mget\n", 5, 0 ); // major change jun 2019
   fflush( boom );
//   sleep( 1 );
//   printf( "cx: %s\n", cx + 1 );
//   send( sock, "provo.utah.us\r\n", 15, 0 );//sis, len_cx, 0 );
//   printf( "%s-%d\n", sis, len_cx );
   send( sock, sis, len_cx, 0 );
   {
               char* rest = NULL;
               int len = 0;
//               getline( &rest, &len, boom );
//               printf( "data: %s\n", rest );
//               free( rest );
   }
   free( sis );
   fflush( boom );
//   sleep( 0.1 );
//   printf( "que\n" );
   send( sock, "\n", 1, 0 );
//   send( sock, "\r\n", 2, 0 );
   {
               char* rest = NULL;
               int len = 0;
//               getline( &rest, &len, boom );
//               printf( "data: %s\n", rest );
               free( rest );
   }
   fflush( boom );
   sleep( 0.1 );
   return boom; // close( sock ) when done.
}

#include <sched.h>

//client connection
void respond(int n, magic_t sis)
{
   char *reqline[3], data_to_send[BYTES];
   char* mesg,* path;
   int rcvd, fd, bytes_read;

   mesg = malloc( 99999 );
   path = malloc( 99999 );
   //cx = malloc( 4096 );
   memset( ( void* )mesg, ( int )'\0', 99999 );
   rcvd = recv( clients[ n ], mesg, 99999, 0 );

   if( rcvd < 0 ) // receive error
      fprintf(stderr, "recv() error\n" );
   else if (rcvd==0) // receive socket closed
      fprintf(stderr,"Client disconnected upexpectedly.\n");
   else // message received
   {
      printf("%s", mesg);
      reqline[ 0 ] = strtok( mesg, " \t\n" );
      if ( strncmp(reqline[ 0 ], "GET\0", 4)==0 )
      {
	 reqline[ 1 ] = strtok( NULL, " \t" );
	 reqline[ 2 ] = strtok( NULL, " \t\n" );
	 if ( strncmp( reqline[ 2 ], "HTTP/1.0", 8) != 0 && strncmp( reqline[ 2 ], "HTTP/1.1", 8 ) != 0 )
	 {
	    write(clients[n], "HTTP/1.0 400 Bad Request\n", 25);
	 }
	 else
	 {
	    int sis, line4s = 0, bah;
	    FILE* boom;
	    if ( strncmp( reqline[ 1 ], "/\0", 2 ) == 0 )
	       reqline[ 1 ] = "/index.html"; // if no file is specified, index.html will be opened as default.

//	    strcpy( path, ROOT );
//	    strcpy( &path[ strlen( ROOT ) ], reqline[ 1 ] );
//	    printf( "file: %s\n", path );

//            sleep( 0.1 );

            clientn = n;
            send( clients[ n ], "HTTP/1.0 200 OK\r\n", 17, 0 );
            send( clients[ n ], "Content-Type: text/plain\r\n", 26, 0 );
            char* allow = "Access-Control-Allow-Origin: *\r\n\r\n";
            send( clients[ n ], allow, strlen( allow ), 0 ); // this worked with xmlhttprequest.
            recent[ 0 ] = '\0';

            boom = query( reqline[ 1 ] ); // /cx

            //boom = fdopen( sis, "rw" );
            for( line4s = 0; line4s < 3; ++line4s )
            {
               char* rest = NULL;
               int len = 0;
//               getline( &rest, &len, boom );
//               printf( "data: %s\n", rest );
               free( rest );
            }
//            sleep( 3 );
            bah = 0;
            while( non < 6 || bah < 99999 )
            {// can we do any of this?
//               io( 0 );
               sleep( 0.001 );
               printf( "x" );
//               sched_yield();
//               break;
               if( ++bah > 99999 )
               {
                  int faz = strlen( reqline[ 1 ] );
                  char* feh = malloc( faz + 13 );
                  strcpy( feh, "not related: " );
                  strcat( feh, reqline[ 1 ] + 1 );
                  printf( "feh: %s; recent: %s", feh, recent );
                  if( strlen( feh ) > 13 )
                  {
                     feh[ 13 ] = '\0';
                     recent[ 13 ] = '\0';
                     if( strcmp( feh, recent ) == 0 )
                        break;
                     else break;
                  }

//                  fclose( boom );
//                  boom = query( reqline[ 1 ] ); // /cx

               }
            }
            fclose( boom );
            printf( "non: %d\n", non );
            non = 0;
            clientn = -1;
//            sleep( 1 );
            sockio = -1;  sockbuf = NULL;
	 }
      }
   }
   //Closing SOCKET
   shutdown( clients[ n ], SHUT_RDWR ); // further send and recieve operations are DISABLED...
   close( clients[ n ] );
   clients[ n ] = -1;
   free( path );
   free( mesg );
}
