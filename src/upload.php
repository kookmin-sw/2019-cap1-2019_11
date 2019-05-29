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
        $output = passthru('cd /home/ubuntu/yoloface/ && ls && python3 yoloface_gpu.py --video /var/www/html/uploads/'.$file_name.' && sudo mv /home/ubuntu/yoloface/outputs/final_yoloface.mp4 /var/www/html/outputs 2>&1');
        echo $output;
    }
    else if(substr($name,-4) == '.jpg')
    {
        $output = passthru('cd /home/ubuntu/yoloface/ && ls && python3 yoloface_img.py --image /var/www/html/uploads/'.$file_name.' && sudo mv /home/ubuntu/yoloface/outputs/final.jpg /var/www/html/outputs 2>&1');
        
        echo $output;
    }
    ?>
