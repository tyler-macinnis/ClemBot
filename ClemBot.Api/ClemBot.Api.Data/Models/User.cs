using System.Collections.Generic;

namespace ClemBot.Api.Data.Models
{
    public class User
    {
        public int Id { get; set; }
        
        public string Name { get; set; }

        public List<Guild> Guilds { get; set; } = new();
        
        public List<Tag> Tags { get; set; } = new();
        
        public List<Message> Messages { get; set; } = new();
    }
}