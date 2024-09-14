export default `
classDiagram

direction LR

        class \`MovieController.java\` {
            Type: File
            Contains: RestAPIController
            Path: .../controller/MovieController.java
        }

        class MovieController{
            Type: Class
            FileName: MovieController.java
        }

        \`MovieController.java\` --|> MovieController : Defines
        
                MovieController : helloWorld() None
                
                MovieController : addMovie(Movie) None
                
                MovieController : getDirectorByMovieId(Long) None
                
        class \`MovieService.java\` {
            Type: File
            Contains: Service
            Path: .../service/MovieService.java
        }

        class MovieService{
            Type: Interface
            FileName: MovieService.java
        }

        \`MovieService.java\` --|> MovieService : Defines
        
                MovieService : addMovie(Movie) None
                
                MovieService : getDirectorByMovieId(Long) None
                
                MovieService : findMovieById(Long) None
                
                MovieService : getAllMovies() None
                
                MovieService : deleteMovieById(Long) None
                
                MovieService : updateMovieById(Long, Movie) None
                
                MovieService : getActorsByMovieId(Long) None
                
                MovieService : addActor(Long, Actor) None
                
        class \`FizzBuzz.java\` {
            Type: File
            Contains: Service
            Path: .../impl/FizzBuzz.java
        }

        class FizzBuzz{
            Type: Class
            FileName: FizzBuzz.java
        }

        \`FizzBuzz.java\` --|> FizzBuzz : Defines
        
                FizzBuzz : checkFizzBuzz(int) None
                
        class \`MovieServiceImpl.java\` {
            Type: File
            Contains: Service
            Path: .../impl/MovieServiceImpl.java
        }

                    class \`MovieService\` {
                    }

                    MovieServiceImpl ..|> \`MovieService\` : Implements
                
        class MovieServiceImpl{
            Type: Class
            FileName: MovieServiceImpl.java
        }

        \`MovieServiceImpl.java\` --|> MovieServiceImpl : Defines
        
                MovieServiceImpl : addMovie(com.movie.movie.entity.Movie) None
                
                MovieServiceImpl : getDirectorByMovieId(Long) None
                
                MovieServiceImpl : findMovieById(Long) None
                
                MovieServiceImpl : getActorsByMovieId(Long) None
                
                MovieServiceImpl : addActor(Long, com.movie.movie.entity.Actor) None
                
                MovieServiceImpl : getAllMovies() None
                
                MovieServiceImpl : deleteMovieById(Long) None
                
                MovieServiceImpl : updateMovieById(Long, com.movie.movie.entity.Movie) None
                
            MovieController --> MovieService : Invokes
            


        class \`Actor.java\` {
            Type: File
            Contains: Model/Entity/DTO
            Path: .../entity/Actor.java
        }

        class Actor {
            Type: Class
            Fields: [

Long id

String name

String biography

Movie movie
]
        }

        \`Actor.java\` --|> Actor : Defines
        
        class \`Crew.java\` {
            Type: File
            Contains: Model/Entity/DTO
            Path: .../entity/Crew.java
        }

        class Crew {
            Type: Class
            Fields: [

Long id

String name

String role
]
        }

        \`Crew.java\` --|> Crew : Defines
        
        class \`Director.java\` {
            Type: File
            Contains: Model/Entity/DTO
            Path: .../entity/Director.java
        }

        class Director {
            Type: Class
            Fields: [

Long id

String name

String biography
]
        }

        \`Director.java\` --|> Director : Defines
        
        class \`Movie.java\` {
            Type: File
            Contains: Model/Entity/DTO
            Path: .../entity/Movie.java
        }

        class Movie {
            Type: Class
            Fields: [

long Id

String title

int releaseYear

String genre

Director director
]
        }

        \`Movie.java\` --|> Movie : Defines
        
`