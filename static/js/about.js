// let formAdd =``;
//     Add = function() {
//         console.log('chaimae')
       
//          let number = $('#wrapper').children().length + 1;
    
//          formAdd = `
    
//          <div class="form-row">
//             <div class="form-group col-md-4">
//                 <label for="produit-1">#${number} Item name </label>
//                 <!-- <input required name="article" type="text" class="form-control" id="article-${number}"> -->
//                  <select name="produit" class="form-control" id="produit">
//                 <option> Choose a product ... </option>
//                 {% for produit in produits %}
//                 <option value="{{produit.id}}"  onkeyup="getTotal(this.id)" >{{forloop.counter}}-{{produit.name}}</option>
//                 {% endfor %}
//             </select>
//             </div>

//             <div class="form-group col-md-2">
//                 <label for="qty-1"> Quantity </label>
//                 <input required name="qty" type="number" min="1" step="0.1" onkeyup="getTotal(this.id)"  class="form-control" id="qty-${number}">
//             </div>

//             <div class="form-group col-md-3">
//                 <label for="unit-1"> Unit Price </label>
//                 <input required name="unit" type="number" min="1" step="0.1" onkeyup="getTotal(this.id)" class="form-control" id="unit-${number}">
               
//             </div>

           
//             <div class="form-group col-md-3">
//                 <label for="total-a-1"> Total </label>
//                 <input required name="total-a" type="number" min="1" step="0.1" readonly class="form-control"
//                     id="total-a-${number}">
//             </div>

//         </div>

//     </div>
//                     `;   
//                     // document.getElementById('more').innerHTML = formAdd;                
        
//         $("#wrapper:last").append(formAdd);          
//     }
    // remove last item line
    remove = function(){
        let num =  $('#wrapper').children().length  ;
        console.log(num);
        let idQty = `#qty-${num}`;
        let unitId = `#unit-${num}`;
        // let total = document.getElementById('total');
        $(`#total`).val(parseFloat($(`#total`).val()) - (parseFloat($(idQty).val()) * parseFloat($(unitId).val())));
        $("#wrapper").children().last().remove()
       
        // console.log(parseFloat($(total).val()));

    }
    // calculer le total
   
    let price;
    let tab = [];
    function getTotal(id){
              
            if ( $('#total').val() == '')
                     $('#total').val(0);
               
               console.log(id.toString().split('-'))
               let articleId = id.split('-')[1];
               
               let idQty = `#qty-${articleId}`;

               let unitId = `#unit-${articleId}`;

               let totalIdLine = `#total-a-${articleId}`;

               let totalLine = parseFloat($(idQty).val()) * parseFloat($(unitId).val());

               $(totalIdLine).val(totalLine);
               tab[articleId] = totalLine;
            //    if (cpt == articleId){ 
            //      result = totalLine;
                    // cpt++;
            //    }
            //    else{ 
                //   result = totalLine;
                // $('#total').val(parseFloat($('#total').val()) + totalLine);
            //    }
            let sum =0 ;
            for (i in tab){
                 sum = sum + tab[i];
                $('#total').val(sum);
            }
    
}
