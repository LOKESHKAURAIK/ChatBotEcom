function chatBot() {
    return {
        botTyping: false,
        messages: [{
            from: 'bot',
            text: 'May I know what is bothering you?'
        }],
        output: function(input) {
            console.log(input);
            this.botTyping = true;
            var product;
            var self = this;
             this.messages.push({
                from: 'user',
                text: input
            });
            this.scrollChat();
            $.ajax({
                type : 'POST',
                url : "/gpt_response",
                contentType: 'application/json;charset=UTF-8',
                data : JSON.stringify({'text':input}),
                success:function(res){
                  console.log(res);
                  product = res;
                  console.log(product);
                  self.messages.push({
                    from: 'bot',
                    text: product
                });
                self.scrollChat();
                self.botTyping = false;
                  self.addChat(input, product);
                  $.get('/get_conversation_id', function (conv_id) {
                    // make ajax call to insert conversation
                    $.ajax({
                      type: 'POST',
                      url: '/conversation',
                      contentType: 'application/json;charset=UTF-8',
                      data: JSON.stringify({
                        id: conv_id,
                        messages: JSON.stringify(self.messages),
                      }),
                      success: function (res) {
                        console.log('Conversation inserted successfully.');
                      },
                      error: function (err) {
                        console.log('Error inserting conversation.');
                      },
                    });
                  });
                }
            });
        },
        addChat: function(input, product) {
            setTimeout(() => {
                this.scrollChat();
            }, 100)
            setTimeout(() => {
//                this.botTyping = false;
//                this.messages.push({
//                    from: 'bot',
//                    text: product
//                });
//                this.scrollChat();
            }, ((product.length / 10) * 1000) + (Math.floor(Math.random() * 2000) + 1500))

        },
        scrollChat: function() {
            const messagesContainer = document.getElementById("messages");
            messagesContainer.scrollTop = messagesContainer.scrollHeight - messagesContainer.clientHeight;
            setTimeout(() => {
                messagesContainer.scrollTop = messagesContainer.scrollHeight - messagesContainer.clientHeight;
            }, 100);
        },
        updateChat: function(target) {
            if (target.value.trim()) {
                this.output(target.value.trim());
                target.value = '';
            }
        }
    }
}