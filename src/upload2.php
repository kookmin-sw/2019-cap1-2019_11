<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<?php
    if($_SERVER['REQUEST_METHOD']=='POST'){
        $file_name = $_FILES['./input.mp4']['name'];
        $file_size = $_FILES['./input.mp4']['size'];
        $file_type = $_FILES['./input.mp4']['type'];
        $temp_name = $_FILES['./input.mp4']['tmp_name'];
        $location = "uploads/";
        move_uploaded_file($temp_name,$location.$file_name);
        echo "/uploads/".$file_name;
    }else{
        echo "Error";
    }
    
    
    echo " check this : ";
    print_r($_FILES);
    
    
//    echo " --------------test -------------------";
    
    putenv("PYTHONIOENCODING=utf-8");
    $name = $file_name;
    if(substr($name,-4) == '.mp4')
    {
        $output = passthru('cd /home/ubuntu/logomode/ && ls && python3 blur_logo.py --input /var/www/html/uploads/'.$file_name.' --output /var/www/html/uploads/final.mp4 && sudo mv /home/ubuntu/logo_mode/outputs/final.mp4 /var/www/html/outputs 2>&1');
        echo $output;
    }
    else if(substr($name,-4) == '.jpg')
    {
        $output = passthru('cd /home/ubuntu/logomode/ && ls && python3 blur_logo.py --input /var/www/html/uploads/'.$file_name.' --output /var/www/html/uploads/final.jpg && sudo mv /home/ubuntu/logo_mode/outputs/final.jpg /var/www/html/outputs 2>&1');
        
        echo $output;
    }
    ?>
